import numpy as np
import cv2
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

height, width =  5,5  #14, 19

objp = np.zeros((width * height, 3), np.float32)
objp[:, :2] = np.mgrid[0:height, 0:width].T.reshape(-1, 2)
objpoints = []
imgpoints = []
gray = 0

images = glob.glob('*.png')
image_run = 0
# images = ['D:\Furrow Vision\PythonProject_Furrow\CameraClibration\Image_Lizbeth.png']

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (height, width), None)

    if ret:
        image_run+=1
        print(f"Running :{fname}")
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (height, width), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

print(f"Image Runs : {image_run}")

cv2.destroyAllWindows()

ret_1, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


# img = cv2.imread(r'image_sensorid_1_frame_23275_ts_1663090405.8703.png')
img = cv2.imread(fname)

h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
dst_1 = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x_1, y_1, w_1, h_1 = roi
dst_1 = dst_1[y_1:y_1 + h_1, x_1:x_1 + w]
cv2.imwrite('calibresult_undistort.png', dst_1)

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
dst_2 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

# crop the image
x_2, y_2, w_2, h_2 = roi
dst_2 = dst_2[y_2:y_2 + h, x_2:x_2 + w]
cv2.imwrite('calibresult_initUnit.png', dst_2)

mean_error = 0
tot_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    tot_error += error

print("total error: ", mean_error / len(objpoints))
