import cv2
import numpy as np

# Apply Harris Corner Algorithm to find maximum rectangle
# Then apply a rotation to the piece, parallel to our wanted plane
from JigsawSolver.test_code.EdgeProcessing.global_config import CANNY_JIGSAW_PATH, CANNY_JIGASW_PIECE, \
    JIGSAW_PIECES_COUNT, FULL_JIGSAW_IMAGE


def harris_subpixel_corner():
    for image_number in range(0, JIGSAW_PIECES_COUNT):
        filename = CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE.format(image_number)

        try:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            dst = cv2.cornerHarris(gray,4,3,0.025)

            #result is dilated for marking the corners, not important
            dst = cv2.dilate(dst,None)

            # Threshold for an optimal value, it may vary depending on the image.
            dst_threshold = 0.25
            img[dst>dst_threshold*dst.max()] = [0,0,255]

            ret, dst = cv2.threshold(dst,dst_threshold*dst.max(),255,0)
            dst = np.uint8(dst)

            try:
                points = find_points(dst, gray)
                #maximum_rectangle_pts(img, points)
                print(minAreaRect(tuple(map(tuple, points))))
            except:
                # No Points found
                pass

            cv2.imshow('piece',img)
            cv2.waitKey(0)


        except:
            raise
            print(filename, ': No corners found')


def find_points(dst, gray):
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    return corners


def maximum_rectangle_pts(pts):
    print(tuple(map(tuple, pts)))


harris_subpixel_corner()

# Python Implementation of above approach
import collections

# function to find minimum area of Rectangle
def minAreaRect(A):

    # creating empty columns
    columns = collections.defaultdict(list)

    # fill columns with coordinates
    for x, y in A:
        columns[x].append(y)

    lastx = {}
    ans = float('inf')

    for x in sorted(columns):
        column = columns[x]
        column.sort()
        for j, y2 in enumerate(column):
            for i in range(j):
                y1 = column[i]

                # check if rectangle can be formed
                if (y1, y2) in lastx:
                    ans = min(ans, (x - lastx[y1, y2]) * (y2 - y1))
                lastx[y1, y2] = x

    if ans < float('inf'):
        return ans
    else:
        return 0

# Driver code
A = [[1, 1], [1, 3], [3, 1], [3, 3], [2, 2]]
print(minAreaRect(A))