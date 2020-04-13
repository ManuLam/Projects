import logging

import cv2
import numpy as np

from global_config import FULL_JIGSAW_IMAGE, HOUGHP_PIECES, HOUGHP_PIECES_PATH, \
    HOUGHP_NON_SIDE_PIECES_PATH, HOUGHP_SIDE_PIECES_PATH

img_c = cv2.imread(FULL_JIGSAW_IMAGE)   # Original Full IMAGE
img_c = cv2.resize(img_c, None, fx=0.80, fy=0.80)  # Resize since image is huge
img_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)  # Convert the image into grey-scale
cv2.imwrite('temp.png', img_c)  # Save this image

original = img_c = cv2.imread('temp.png')  # Load the gray scale image back up

logger = logging.getLogger(__name__)  # For logging purposes


def locate_straight_sides_list(filename_list, full_display=False, show=False):
    """
    This function goes through all the files in a list and detects straight lines, writes to the files passed

    :param filename_list: A list of files that we want to detect lines in
    :param full_display: A boolean that can allow us to write to the Original Full image
    :param show: A boolean that can allow us to see the progress
    """

    # Draw all the detected lines back on our passed image (and Original if wanted)
    for file in filename_list:
        straight_edge_count = 0
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 75, 150)

        try:
            # Returns list of lines detected with HoughLinesP
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
            cv2.imshow("linesDetected", img)  # Show this Image
            cv2.waitKey(0)  # Waits until user input a keystroke


def locate_straight_side_img(img, full_display=False, min_line_length=55, max_line_gap=10, show=False):
    """
    This function locates all the straight edges within an image and then returns 1 or 0

    :param img: The image we want to scan for lines
    :param full_display: Input for allowing us to write to the Full Original image
    :param min_line_length: Input for the minimum line length to be detected
    :param max_line_gap: Input threshold for the maximum gap the located line can have
    :param show: A boolean that can show the progress
    :return: 0 or 1 - 0 implies that no straight edges are found, 1 implies that at least 1 straight edge is found
    """

    straight_edge_count = 0     # 0 Flat Edges at start
    edges = cv2.Canny(img, 75, 150)  # Save the img and apply CannyEdge to it

    try:
        # Returns list of lines detected with HoughLinesP
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=min_line_length, maxLineGap=max_line_gap)

        # Draw all the detected lines back on our passed image (and Original if wanted)
        for line in lines:
            x1, y1, x2, y2 = line[0]                                    # Extract Line coordinates from lines List
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)           # Draw line on input image
            if full_display:
                cv2.line(original, (x1, y1), (x2, y2), (0, 255, 0), 1)  # Draw line on Full Original image

        straight_edge_count = len(lines)        # store the total amount of lines found

    except:
        pass

    logger.info('Sides detected : %d', straight_edge_count)

    # Show the progress of the HoughLinesP (Useful for debugging)
    if show:
        cv2.imshow("linesDetected", img)  # Show the input image with the detected lines
        cv2.waitKey(0)  # Waits until user input a keystroke

    return min(1, straight_edge_count)  # Returns 0 or 1


def locate_full_canny_straight_sides(filename_list):
    """
    This function calls locate_straight_sides_list and turns on the Full Display, allow us to write to the
    Full Original image as well as the passed list

    :param filename_list: A List of files that we want to detect edges on
    """

    locate_straight_sides_list(filename_list, full_display=True)  # Locates straight edges on a list

    cv2.imwrite('Hough_Lines_P_Detected.png', original)  # Save this image after detecting lines
    cv2.imshow("linesDetected", original)   # Show this Image

    cv2.waitKey(0)  # Waits until user input a keystroke
