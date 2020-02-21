import cv2
import numpy as np

# Sides to detail / Enrichment of pieces
# GREEN = SIDE
# RED = OUTER
# BLUE = INNER

# Quickly save an image to gray scale
from JigsawSolver.test_code.EdgeProcessing.global_config import FULL_JIGSAW_IMAGE, FULL_IMAGE_CANNY_JIGSAW_PATH, \
    FULL_IMAGE_CANNY_JIGASW_PIECE, SIDE_PIECES_BOX, JIGSAW_PIECES_COUNT, HOUGHP_PIECES, HOUGHP_PIECES_PATH, \
    ROTATED_PIECES, ROTATED_PIECES_PATH, HOUGHP_NON_SIDE_PIECES_PATH, HOUGHP_SIDE_PIECES_PATH

img_c = cv2.imread(FULL_JIGSAW_IMAGE)
img_c = cv2.resize(img_c, None, fx=0.80, fy=0.80)  # resize since image is huge
img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
cv2.imwrite('temp.png', img_c)

# Load the gray scale back up
original = img_c = cv2.imread('temp.png')


def locate_straight_sides(filename_list, full_display=False):
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

                print(((x2 - x1)**2 + (y2 - y1)**2)**.5)

            cv2.imshow("linesDetected", img)
            straight_edge_count = len(lines)
            print(file, straight_edge_count)

            if straight_edge_count > 0:
                cv2.imwrite(HOUGHP_PIECES_PATH + HOUGHP_SIDE_PIECES_PATH + HOUGHP_PIECES.format(filename_list.index(file)), img)

            cv2.waitKey(0)

        except:
            print('Not Side / Corner piece')

            img = cv2.imread(file)
            cv2.imwrite(HOUGHP_PIECES_PATH + HOUGHP_NON_SIDE_PIECES_PATH + HOUGHP_PIECES.format(filename_list.index(file)), img)
            cv2.imshow("linesDetected", img)
            cv2.waitKey(0)


def locate_full_canny_straight_sides(filename_list):
    locate_straight_sides(filename_list, full_display=True)

    cv2.imwrite('Hough_Lines_P_Detected.png', original)
    cv2.imshow("linesDetected", original)

    cv2.waitKey(0)


def locate_inner_outter_piece():
    1


# Apply HoughLines P onto each Rotated Jigsaw piece to find side edges
locate_straight_sides([ROTATED_PIECES_PATH + ROTATED_PIECES.format(image_number) for image_number in range(0, JIGSAW_PIECES_COUNT)])

# Apply HoughLines P onto Entire canny edged image
# locate_full_canny_straight_sides([FULL_IMAGE_CANNY_JIGSAW_PATH + FULL_IMAGE_CANNY_JIGASW_PIECE.format(image_number) for image_number in range(0, JIGSAW_PIECES_COUNT)])
print(SIDE_PIECES_BOX)
