import logging

import cv2
import numpy as np

from global_config import FULL_JIGSAW_IMAGE, HOUGHP_PIECES, HOUGHP_PIECES_PATH, \
    HOUGHP_NON_SIDE_PIECES_PATH, HOUGHP_SIDE_PIECES_PATH

img_c = cv2.imread(FULL_JIGSAW_IMAGE)
img_c = cv2.resize(img_c, None, fx=0.80, fy=0.80)  # resize since image is huge
img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
cv2.imwrite('temp.png', img_c)

# Load the gray scale back up
original = img_c = cv2.imread('temp.png')

logger = logging.getLogger(__name__)


def locate_straight_sides_list(filename_list, full_display=False, show=False):
    for file in filename_list:
        straight_edge_count = 0
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)

        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=12)

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                if full_display:
                    cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)

            straight_edge_count = len(lines)

            if straight_edge_count > 0:
                cv2.imwrite(HOUGHP_PIECES_PATH + HOUGHP_SIDE_PIECES_PATH + HOUGHP_PIECES.format(filename_list.index(file)), img)

        except:
            img = cv2.imread(file)
            cv2.imwrite(HOUGHP_PIECES_PATH + HOUGHP_NON_SIDE_PIECES_PATH + HOUGHP_PIECES.format(filename_list.index(file)), img)

        logger.info(' %s Sides detected : %d', file, straight_edge_count)

        if show:
            cv2.imshow("linesDetected", img)
            cv2.waitKey(0)


def locate_straight_side_img(img, full_display=False, show=False):
        straight_edge_count = 0
        edges = cv2.Canny(img, 75, 150)

        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=65, maxLineGap=12)

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                if full_display:
                    cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)

            straight_edge_count = len(lines)

        except:
            pass

        logger.info('Sides detected : %d', straight_edge_count)

        if show:
            cv2.imshow("linesDetected", img)
            cv2.waitKey(0)

        return min(1, straight_edge_count)


def locate_full_canny_straight_sides(filename_list):
    locate_straight_sides_list(filename_list, full_display=True)

    cv2.imwrite('Hough_Lines_P_Detected.png', original)
    cv2.imshow("linesDetected", original)

    cv2.waitKey(0)
