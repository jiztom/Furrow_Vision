import cv2
import numpy as np
import glob
from matplotlib import pyplot as plt
import pathlib as pt
import pandas as pd
import scipy.io as sio

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

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

data_x = []
data_y = []
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
                dict_temp['mmPerPixel'] = ground_truth / dict_temp['diff']
                data_x.append(dict_temp)
        for col in range(Y.shape[1]):
            x_mean = int(np.median(X[:, col]))
            y_mean = int(np.median(Y[col]))
            # y_mean = 100
            for row in range(Y.shape[0]-1):
                dict_y = {
                    'Y1': Y[row][col],
                    'Y2': Y[row+1][col],
                    'X': x_mean,
                    'Y': y_mean,
                    'diff': abs(Y[row][col] - Y[row+1][col]),
                    'ground': ground_truth,
                    }
                dict_y['mmPerPixel'] = ground_truth / dict_y['diff']
                data_y.append(dict_y)
        if fig_show:
            temp_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(10, 10))
            plt.imshow(temp_img)
            plt.show()

df_x = pd.DataFrame(data_x)
df_y = pd.DataFrame(data_y)
# df.to_excel("Calibration_Data.xlsx")

xx, xy = df_x['Y'], df_x['mmPerPixel']

yx, yy = df_y['Y'], df_y['mmPerPixel']
# # create scatter plot
# plt.scatter(x, y)
#
# # calculate equation for trend-line
# z = np.polyfit(x, y, 2)
# p = np.poly1d(z)
#
# # add trend-line to plot
# plt.plot(x, p(x))
#
# plt.show()

poly = PolynomialFeatures(degree=4)
x_re = xx.values.reshape((-1, 1))
X_poly = poly.fit_transform(x_re)
poly.fit(X_poly, xy)
lin2 = LinearRegression()
lin2.fit(X_poly, xy)

# Visualising the Polynomial Regression results
plt.scatter(x_re, xy, color='blue')

plt.plot(x_re, lin2.predict(poly.fit_transform(x_re)), color='red')
plt.title('X Polynomial Regression')
plt.xlabel('Y position')
plt.ylabel('mmPerPixel')

plt.show()
# ------------
poly = PolynomialFeatures(degree=4)
y_re = yx.values.reshape((-1, 1))
Y_poly = poly.fit_transform(y_re)
poly.fit(Y_poly, yy)
lin2 = LinearRegression()
lin2.fit(Y_poly, yy)

# Visualising the Polynomial Regression results
plt.scatter(y_re, yy, color='blue')

plt.plot(y_re, lin2.predict(poly.fit_transform(y_re)), color='red')
plt.title('Y Polynomial Regression')
plt.xlabel('X position')
plt.ylabel('mmPerPixel')

plt.show()


# import pickle
#
# save_name = 'Linear_reg.pkl'
# with open(save_name, 'wb') as file:
#     pickle.dump(lin2, file)
#
# with open(save_name, 'rb') as file:
#     pickle_model = pickle.load(file)
