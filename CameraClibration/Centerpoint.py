import cv2
import numpy as np

img = cv2.imread(r'D:\Furrow Vision\PythonProject_Furrow\CameraClibration\Images'
                 r'\image_sensorid_1_frame_43389_ts_1663090741.2430.png')

# get image height, width
(h, w) = img.shape[:2]

# calculate the center of the image
center = (w / 2, h / 2)
scale = 1.0

# Perform the counter clockwise rotation holding at the center
# 90 degrees
M = cv2.getRotationMatrix2D(center, 180, scale)
img = cv2.warpAffine(img, M, (w, h))
# img = cv2.rotate(img, cv2.ROTATE_180)
lower_red_mask1 = np.array([80, 0, 252])
upper_red_mask1 = np.array([94, 91, 255])

mask_size = 5

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask_1 = cv2.inRange(hsv, lower_red_mask1, upper_red_mask1)
mask = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((mask_size, mask_size), np.uint8))
# # convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = 255 - gray
#
# # threshold
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
# thresh = 255 - thresh
#
# # apply close to connect the white areas
# kernel = np.ones((3, 3), np.uint8)
# morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
# kernel = np.ones((1, 9), np.uint8)
# morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

# apply canny edge detection
edges = cv2.Canny(mask_1, 150, 200)

# get hough lines
result = img.copy()
lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
# Draw line on the image
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 1)

x_mid = int((img.shape[1])/2)
y_mid = int(np.floor(y0))
cv2.circle(result, (x_mid, y_mid), radius=3, color=(0, 0, 255), thickness=-1)
cv2.circle(result, (310, 378), radius=3, color=(0, 255, 255), thickness=-1)
print(f'Center Point in image with respect to the line = [{x_mid},{y_mid}]')
# # save resulting images
# cv2.imwrite('fft_thresh.jpg', hsv)
# cv2.imwrite('fft_morph.jpg', mask_1)
# cv2.imwrite('fft_edges.jpg', edges)
# cv2.imwrite('fft_line.jpg', result)

# show thresh and result
# cv2.imshow("thresh", hsv)
# cv2.imshow("morph", mask_1)
# cv2.imshow("edges", edges)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 310,378 was assumed to the final center point of the GPS
