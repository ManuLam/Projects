import cv2
import numpy as np

# Sides to detail / Enrichment of pieces
# GREEN = SIDE
# RED = OUTER
# BLUE = INNER

# Quickly save an image to gray scale
from JigsawSolver.test_code.EdgeProcessing.global_config import FULL_JIGSAW_IMAGE, FULL_IMAGE_CANNY_JIGSAW_PATH, \
    FULL_IMAGE_CANNY_JIGASW_PIECE, SIDE_PIECES_BOX, JIGSAW_PIECES_COUNT

img_c = cv2.imread(FULL_JIGSAW_IMAGE)
img_c = cv2.resize(img_c, None, fx=0.80, fy=0.80)  # resize since image is huge
img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
cv2.imwrite('temp.png', img_c)

# Load the gray scale back up
original = img_c = cv2.imread('temp.png')


def locate_straight_sides():
    for image_number in range(0, JIGSAW_PIECES_COUNT):
        straight_edge_count = 0
        filename = FULL_IMAGE_CANNY_JIGSAW_PATH + FULL_IMAGE_CANNY_JIGASW_PIECE.format(image_number)
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)

        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=10)
            #lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=10)

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)

                print(((x2 - x1)**2 + (y2 - y1)**2)**.5)

            cv2.imshow("linesDetected", img)
            straight_edge_count = len(lines)
            print(filename, straight_edge_count)
            cv2.waitKey(0)

        except:
            print('Not Side / Corner piece')
            img = cv2.imread(filename)
            cv2.imshow("linesDetected", img)
            cv2.waitKey(0)

        if straight_edge_count > 0:
            SIDE_PIECES_BOX.append(filename)

    cv2.imwrite('Hough_Lines_P_Detected.png', original)
    cv2.imshow("linesDetected", original)

    cv2.waitKey(0)


def locate_inner_outter_piece():
    1


locate_straight_sides()
print(SIDE_PIECES_BOX)
