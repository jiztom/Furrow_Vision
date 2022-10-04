import cv2
import numpy as np
import glob
from matplotlib import pyplot as plt
import pathlib as pt
import pandas as pd
import scipy.io as sio

ground_truth = 30
fig_show = False
# Defining the dimensions of checkerboard
CHECKERBOARD = (5, 7)
data = sio.loadmat('data.mat')
mtx, dist, rvecs, tvecs = data['camera_matrix'], data['dist_coeff'], data['rvecs'], data['tvecs']

# ---------------------------- Typing Font infomration -----------------------
# font
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (255, 0, 0)
thickness = 1

inver_chess = CHECKERBOARD[::-1]
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Extracting path of individual image stored in a given directory
images = glob.glob(r'D:\Furrow Vision\PythonProject_Furrow\CameraClibration\Images\*.png')

data = []

for fname in images:
    name = pt.Path(fname)
    img = cv2.imread(fname)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    img = dst
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret:
        X, Y = np.zeros(inver_chess, int), np.zeros(inver_chess, int)
        j = -1
        for pos, cor in enumerate(corners):
            x, y = cor.ravel()
            img = cv2.putText(img, str(pos + 1), (int(x), int(y)), font,
                              fontScale, color, thickness, cv2.LINE_AA)

            if pos % CHECKERBOARD[0] == 0:
                j += 1
            X[j][pos % CHECKERBOARD[0]] = x
            Y[j][pos % CHECKERBOARD[0]] = y

        for row in range(len(X)):
            y_mean = int(np.median(Y[row]))

            for col in range(X.shape[1] - 1):
                dict_temp = {'X1': X[row][col],
                             'X2': X[row][col + 1],
                             'Y': y_mean,
                             'image_source': name.stem,
                             'diff': abs(X[row][col] - X[row][col + 1]),
                             'ground': ground_truth}
                dict_temp['inchPerPixel'] = ground_truth / dict_temp['diff']
                data.append(dict_temp)
        if fig_show:
            temp_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(10, 10))
            plt.imshow(temp_img)
            plt.show()

df = pd.DataFrame(data)
df.to_excel("Calibration_Data.xlsx")

x, y = df['Y'], df['inchPerPixel']
# create scatter plot
plt.scatter(x, y)

# calculate equation for trend-line
z = np.polyfit(x, y, 2)
p = np.poly1d(z)

# add trend-line to plot
plt.plot(x, p(x))

plt.show()
