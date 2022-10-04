import cv2
import json
import scipy.io as sio

data = sio.loadmat('data.mat')
mtx, dist, rvecs, tvecs = data['camera_matrix'], data['dist_coeff'], data['rvecs'], data['tvecs']

img = cv2.imread(
    'D:\Furrow Vision\PythonProject_Furrow\CameraClibration\Images\image_sensorid_1_'
    'frame_43345_ts_1663090740.5094.png')

h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
cv2.imwrite('calibresult_jiztom.png', dst)

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
cv2.imwrite('calibresult-distort.png', dst)
