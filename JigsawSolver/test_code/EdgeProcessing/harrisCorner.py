import cv2
import numpy as np

# Apply Harris Corner Algorithm to find maximum rectangle
# Then apply a rotation to the piece, parallel to our wanted plane

filename = '../pieces/test_JIGSAW_PIECE_0.png'
img = cv2.imread(filename)


def max_rectangke_harris_corner():
    for i in range(0,13,1):
        filename = '../pieces/test_JIGSAW_PIECE_{}.png'.format(i)

        try:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            dst = cv2.cornerHarris(gray,4,3,0.04)

            #result is dilated for marking the corners, not important
            dst = cv2.dilate(dst,None)
            pts_for_rect(dst.max())
            # Threshold for an optimal value, it may vary depending on the image.
            img[dst>0.125*dst.max()] = [0,0,255]
            cv2.imshow('piece',img)
            cv2.waitKey(0)

        except:
            print(filename, ': No corners found')


def pts_for_rect(pts):
    print(pts)

max_rectangke_harris_corner()
