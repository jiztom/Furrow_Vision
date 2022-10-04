import numpy as np

# https://medium.com/swlh/image-processing-with-python-image-warping-using-homography-matrix-22096734f09a# to calculate the transformation matrix
input_pts = np.float32([[750, 0], [1170, 0], [1880, 1080], [40, 1080]])
output_pts = np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]])

# # Compute the perspective transform M
# M = cv2.getPerspectiveTransform(input_pts, output_pts)
#
# # Apply the perspective transformation to the image
# out = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
#
# # resize image
# resized = cv2.resize(out, dim, interpolation=cv2.INTER_AREA)