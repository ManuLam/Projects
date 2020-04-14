import math

import cv2
import numpy as np
from global_config import colours

corner_index_pairs = {'BOT': (0, 1), 'LEFT': (0, 3), 'RIGHT': (1, 2), 'TOP': (2, 3)}  # Order we will create/match lines
colour_array = [colours['AQUA'], colours['GREEN'], colours['BLUE'], colours['RED']]  # Colours in this order B/L/R/T


def draw_lines_from_corner(img, pts):
    """
    Joins all pairs of points to form lines.
    These lines are then drawn onto the image being passed.

    :param img: Image of Jigsaw Piece
    :param pts: List of tuples points
    """
    for key in corner_index_pairs.keys():
        p1,p2 = corner_index_pairs[key]
        cv2.line(img, (pts[p1][0], pts[p1][1]), (pts[p2][0], pts[p2][1]),
                 colour_array[list(corner_index_pairs.keys()).index(key)], thickness=1, lineType=8)


def compute_lines_param(pt1, pt2):
    """
    Computes the Line parameter given 2 points
    General Equation of a line Ax + By = C

    :param pt1: Input of point 1
    :param pt2: Input of point 2
    :return: Returns A,B,C of the Line equation
    """

    x0, y0 = pt1[0], pt1[1]  # Extract 1st point
    x1, y1 = pt2[0], pt2[1]  # Extract 2nd point
    return y1-y0, x0-x1, x1*y0 - x0*y1


def compute_lines_params(pts):
    """
    Computes the Line parameter for multiple points pairs by calling compute_lines_param()
    General Equation of a line Ax + By = C

    :param pts: A list of points
    :return: A list of Line parameters of form of A,B,C
    """

    return [compute_lines_param(pts[p1], pts[p2]) for p1, p2 in corner_index_pairs.values()]


def point_to_line_dist_abs(x, y, line_params):
    """
    Compute the absolute distance from a point to a line

    :param x: Input x coordinate of the point
    :param y: Input y coordinate of the point
    :param line_params: Line parameters of form A,B,C
    :return: The absolute distance between a point and the passed Line
    """

    A,B,C = line_params[0], line_params[1], line_params[2]  # Extract A,B,C from line_params list
    return abs((A*x) + (B*y) + C) / math.sqrt(A*A + B*B)


def point_to_line_dist(x, y, line_params):
    """
    Compute the distance from a point to a line

    :param x: Input x coordinate of the point
    :param y: Input y coordinate of the point
    :param line_params: Line parameters of form A,B,C
    :return: The distance between a point and the passed Line
    """

    A,B,C = line_params[0], line_params[1], line_params[2]  # Extract A,B,C from line_params list
    return ((A*x) + (B*y) + C) / math.sqrt(A*A + B*B)


def classify_jigsaw_edges(edges, corners, threshold=5, show=False):
    """
    This function takes an image, 4 tuple pairs of corners and forms lines for classifying side types.
    It goes through every pixel and compares which line it is closest to, if it breaks the threshold, The k nearest neighbour
    is applied.
    It then returns an enhanced image that is coloured based on which side it is.

    :param edges: The pixels of our image
    :param corners: A tuple of 2 corner points (pt1, pt2)
    :param threshold: A threshold for comparing the point of pixel to a line, if it exceeds we will apply k nearest neighbour
    :param show: A boolean to show the progress of our work
    :return: A classified image based on what side it is (BOTTOM/LEFT/RIGHT/TOP)
    """

    lines = compute_lines_params(corners)  # From the corners list tuple, we form line parameters from each pair
    ys, xs, _ = np.nonzero(edges)  # Extract the y and x coordinates from the pixels of our image
    image_classifier = np.zeros(edges.shape, dtype='uint8')  # Create a new pixel image of the same size

    unclassified_points = []  # A List that will contain all points that breach a certain threshold

    # Go through all the points (For each point)
    for x, y in zip(xs, ys):
        # Get a list of distances, for each point to the 4 lines created
        distance_from_lines = [point_to_line_dist_abs(x, y, line) for line in lines]

        if show:  # If we want to see the progress
            cv2.imshow('show', image_classifier)  # Show each point being updated with colours
            cv2.waitKey(1)  # 1 millisecond delay on pixel update

        if np.min(distance_from_lines) < threshold:  # If the point is within our threshold
            image_classifier[y, x] = colour_array[np.argmin(distance_from_lines)]  # Colour the pixel with closest Line
        else:
            unclassified_points.append((x, y))  # Add this point to a List that will be worked with later

    # K Nearest Neighbour algorithm
    unclassified_points = np.array(unclassified_points) # Declare a NumPy Array
    iteration = 0   # Declare the current iteration
    max_iterations = 20  # Allow 20 iterations
    k_distance = 11  # How many neighbours to check for

    while iteration < max_iterations:
        iteration += 1  # Loop upwards
        for (x, y) in unclassified_points:  # Go through the points as x,y
            neighborhood = image_classifier[y - k_distance: y + k_distance, x - k_distance: x + k_distance]  # Looking at our neighbours
            neighbours_mapped = np.nonzero(neighborhood)    # all the neighbours returned (non zero pixels)

            if len(neighbours_mapped[0]) > 0:
                ny, nx = neighbours_mapped[0][0] - k_distance, neighbours_mapped[1][0] - k_distance  # Within our neighbourhood take the k pixel
                image_classifier[y, x] = image_classifier[y + ny, x + nx]  # Update our image with the neighbours pixels' colour

    return image_classifier


def inner_outer_classifier(piece, sides):
    """
    This function is the 2nd Classifier for colouring Jigsaw pieces based off edge type.

    FLAT edge = GREEN
    OUTER edge = RED
    INNER edge = BLUE

    :param piece: image of Jigsaw piece to be recoloured
    :param sides: 4 Line parameters that define the sides
    :return: A new classified image based on edge type
    """

    h, w, _ = cv2.imread(piece.image_file).shape  # Read in the original Jigsaw piece's dimensions
    temp_image = 'temp_side_image.png'  # temporary image name
    template_image = np.zeros((h, w, 3), np.uint8)  # Creating a template image that gets updated

    # Go through all 4 sides of the piece and colour them
    for side in sides:
        cv2.imwrite(temp_image, side['pixels'])  # takes the passed Jigsaw piece's side and writes on the temp image
        side_image = cv2.imread(temp_image)  # Read the temp image

        ys,xs,z = np.nonzero(side_image)  # Take all the pixels
        image_classifier = np.zeros(side_image.shape, np.uint8)  # create a new image

        def colour_edges(side_type, colour):
            """
            This function takes a side type and the colour and if the side matches, we colour that side

            :param side_type: OUT/FLAT/IN
            :param colour: RED/GREEN/BLUE
            """

            if side['edge_type'] == side_type:     # If the side is matched
                for x, y in zip(xs, ys):
                    image_classifier[y, x] = colour   # Colour the image side

        colour_edges('OUT', colours['RED'])     # Colour Outer edge type with RED
        colour_edges('FLAT', colours['GREEN'])  # Colour Flat edge type GREEN
        colour_edges('IN', colours['BLUE'])     # Colour Inner edge type BLUE

        dst = cv2.addWeighted(template_image, 1, image_classifier, 1, 0.0)  # Merge two images together
        template_image = dst   # Update the template image

    return template_image
