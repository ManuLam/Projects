import cv2
import numpy as np

img = cv2.imread('jigsaw_temp_imgs/jigsaw_pieces.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)

rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img,[box],0,(0,0,255),2)

cv2.imshow('dst',img)
cv2.waitKey(0)