
import logging
import math

import cv2
import numpy as np
import operator
from functools import reduce
from scipy.stats import norm
from scipy.spatial.distance import cdist
from global_config import ORIGINAL_JIGSAW_PATH, ORIGINAL_JIGASW_PIECE, CANNY_JIGSAW_PATH, CANNY_JIGASW_PIECE, \
    JIGSAW_PIECES_COUNT, ROTATED_ORIGINAL_PIECES_PATH, ROTATED_ORIGINAL_CANNY_PIECES, ROTATED_CANNY_PIECES_PATH, ROTATED_CANNY_PIECES, HARRIS_PIECES_PATH, HARRIS_PIECES, \
    CLASSIFICATION_PATH, CLASSIFICATION_PIECE, ENRICHED_EDGE_CLASSIFIER_PIECES_PATH, ENRICHED_EDGE_CLASSIFIER_PIECE, ENRICHED_INNER_OUTER_PIECES_PATH, \
    ENRICHED_INNER_OUTER_PIECE,colours
from compute_sides import draw_lines_from_corner, classify_jigsaw_edges, compute_lines_params
from JigsawPiece import JigsawPiece

logger = logging.getLogger(__name__)


def rotate_image(image, degrees):
    """
    This function rotates an image relative to the input degrees parameter

    :param image: The image we want to rotate
    :param degrees: The amount we want to rotate by
    :return: The rotated image and the transposed matrix
    """

    if len(image.shape) == 3:       # extracting the image detail
        rows, cols, _ = image.shape
    else:
        rows, cols = image.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), degrees, .75)     # get 2d rotation matrix and resize

    return cv2.warpAffine(image, M, (cols, rows)), M    # Returns the rotated image and the Transposed Matrix


def sort_points_clockwise(pts):
    """
    This function takes in a list of points and sorts it in a clockwise order

    :param pts: A list of pts to be sorted
    :return: A sorted list of pts in clockwise order
    """

    # Sort clockwise
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), pts), [len(pts)] * 2))
    return sorted(pts, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)


def harris_corner_with_rotation(show=True):
    """
    This function finds all Corner points per Jigsaw piece and the maximum rectangle that can fit
    It then rotate the image based off the rectangle and stores the rotated value
    Also classifies the Jigsaw piece based off side and edge type
    Creates the Jigsaw Piece Object and passes this into a List

    :param show: A boolean to show the progress of the work
    :return: A List of Jigsaw Pieces created
    """

    jigsaw_pieces = []  # A list of Jigsaw Pieces

    # Loop through all the Jigsaw pieces
    for image_number in range(0, JIGSAW_PIECES_COUNT):
        # Formatting file names
        original_filename = ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE.format(image_number)
        canny_filename = CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE.format(image_number)

        try:
            # Reading in files
            harris_img = cv2.imread(canny_filename)
            rotated_harris_image = cv2.imread(canny_filename)
            rotated_classifier_img = cv2.imread(canny_filename)
            rotated_img_canny = cv2.imread(canny_filename)
            rotated_img_original = cv2.imread(original_filename)

            gray = cv2.cvtColor(harris_img, cv2.COLOR_BGR2GRAY)  # Turn Harris Image into greyscale
            gray = np.float32(gray)
            dst = cv2.cornerHarris(gray, 4, 3, 0.04)

            # result is dilated for marking the corners, not important
            dst = cv2.dilate(dst, None)

            # Threshold for an optimal value, it may vary depending on the image.
            dst_threshold = 0.20
            harris_img[dst > dst_threshold * dst.max()] = [0, 0, 255]

            ret, dst = cv2.threshold(dst, dst_threshold * dst.max(), 255, 0)
            dst = np.uint8(dst)

            try:
                points = find_points(dst, gray)
                intersections = get_best_fitting_rect_coords(points, perpendicular_angle_threshold=30)

                if intersections is None:
                    raise RuntimeError('No rectangle found')  # Raise exception here because we must locate a rectangle within our Jigsaw Piece

                if intersections[1, 0] == intersections[0, 0]:
                    rotation_angle = 90
                else:
                    rotation_angle = np.arctan2(intersections[1, 1] - intersections[0, 1], intersections[1, 0] - intersections[0, 0]) * 180 / np.pi

                corners = []
                # Marking the 4 best corners, also giving each corner a thicker green pixel
                for x, y in intersections:
                    rotated_harris_image[int(y)-2:int(y)+2, int(x)-2:int(x)+2] = (0, 255, 0)
                    corners.append([int(x), int(y)])

                # To Avoid diagonal matching, we sort the corners
                corners = sort_points_clockwise(corners)
                draw_lines_from_corner(rotated_classifier_img, corners)

                # Rotate jigsaw images by rotation_angle
                rotated_gray1, M1 = rotate_image(harris_img, rotation_angle)
                rotated_gray2, M2 = rotate_image(rotated_harris_image, rotation_angle)
                rotated_gray3, M3 = rotate_image(rotated_classifier_img, rotation_angle)

                ####################
                # Extract edges and define them as In or Out, must rotate corner points
                rotated_gray4, M4 = rotate_image(rotated_img_canny, rotation_angle)   # Untouched canny image that is rotated
                rotated_original, M5 = rotate_image(rotated_img_original, rotation_angle)   # Untouched original image that is rotated
                rotated_corners = np.array(np.round([M3.dot((point[0], point[1], 1)) for point in corners])).astype(np.int)  # Rotate corner points

                image_classifier = classify_jigsaw_edges(rotated_gray4, rotated_corners)  # Classify jigsaw edges to 4 sides
                ####################

                logger.info("%s rotated by %d degrees", canny_filename, rotation_angle)

            except:
                logger.info("No points found for: ", canny_filename)
                pass

            # Write all the Images to their corresponding DIR
            cv2.imwrite(HARRIS_PIECES_PATH + HARRIS_PIECES.format(image_number), harris_img)
            cv2.imwrite(ROTATED_ORIGINAL_PIECES_PATH + ROTATED_ORIGINAL_CANNY_PIECES.format(image_number), rotated_original)
            cv2.imwrite(ROTATED_CANNY_PIECES_PATH + ROTATED_CANNY_PIECES.format(image_number), rotated_gray2)
            cv2.imwrite(CLASSIFICATION_PATH + CLASSIFICATION_PIECE.format(image_number), rotated_gray3)
            cv2.imwrite(ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE.format(image_number), image_classifier)

            # Create a jigsaw piece object that can later be used for solving the puzzle
            new_jigsaw_piece = JigsawPiece(ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE.format(image_number),
                                           rotation_angle,
                                           compute_lines_params(rotated_corners),
                                           find_centroid(rotated_corners))

            sides = new_jigsaw_piece.get_sides()  # Return all 4 sides of the Jigsaw Piece (Bottom/Left/Right/Top)
            new_classified_inner_outer = inner_outer_classifier(new_jigsaw_piece, sides)  # Classify image based off Edge type

            # Set the file image for the current created Jigsaw Piece Object as the new classified image, with edge types
            new_jigsaw_piece.set_image_file(ENRICHED_INNER_OUTER_PIECES_PATH + ENRICHED_INNER_OUTER_PIECE.format(image_number))
            # Save the newly created Classified Jigsaw Piece with Edge types
            cv2.imwrite(ENRICHED_INNER_OUTER_PIECES_PATH + ENRICHED_INNER_OUTER_PIECE.format(image_number), new_classified_inner_outer)

            # Add the newly created Jigsaw piece to our Jigsaw list
            jigsaw_pieces.append(new_jigsaw_piece)

            # Shows all progress of pieces if set to true
            if show:
                cv2.imshow('harris_img', harris_img)
                cv2.imshow('rotated_harris_img', rotated_gray1)
                cv2.imshow('rotated_maximum_rect', rotated_gray2)
                cv2.imshow('four_line_classifier', rotated_gray3)
                cv2.imshow('side_type_classifier', image_classifier)
                cv2.imshow('edge_type_classifier', new_classified_inner_outer)

                cv2.waitKey(0)  # Waits until user input a keystroke

        except:
            logger.info('No corners found for: ', canny_filename)

    return jigsaw_pieces


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


def find_centroid(pts):
    """
    This function takes in a list of points and then compute the centroid based off all points

    :param pts: Input List of points
    :return: Centroid of all the points
    """

    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    return sum(x) / len(pts), sum(y) / len(pts)


def find_points(dst, gray):
    """
    This function returns all the points back on an image that is dilated

    :param dst: The Dilated locations
    :param gray: A grey-scale image
    :return: Points of all the Harris Corner points
    """

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    points = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria) # Returns the subpixel points from HarrisCorner points

    return points


def compute_list_of_angles(pts):
    """
    This function takes in a List of points and computes all the angles between all the points

    :param pts: A List of points
    :return: A List of angles created from all points passed in
    """

    N = len(pts)
    angles_list = np.zeros((N, N))  # Create NxN NumPy matrix of 0s, we will later store angles into here

    # Looping through the entire array, and combining every other point with this current point to calculate an angle
    for pt1_index in range(N):
        for pt2_index in range(pt1_index + 1, N):
            x, y = pts[pt1_index], pts[pt2_index]  # Extract the two points at the looped array

            # If angle is perpendicular, 90 Degrees else calculate the angle between the two points
            angle = 90 if x[0] == y[0] else (np.arctan2(y[1] - x[1], y[0] - x[0]) * 180) / np.pi
            angles_list[pt1_index, pt2_index], angles_list[pt2_index, pt1_index] = angle, angle

    return angles_list


def polygon_area(x, y):
    """
    This function returns the polygon area, given a set of x and y coordinates

    :param x: List of x coordinates
    :param y: List of y coordinates
    :return: The area of the polygon based off the x and y coordinates
    """

    correction = x[-1] * y[0] - y[-1] * x[0]
    main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
    return 0.5 * np.abs(main_area + correction)


def get_best_fitting_rect_coords(pts, distance_threshold=30, perpendicular_angle_threshold=20):
    """
    This function returns the maximum rectangle possible with a List of points passed

    :param pts: List of points
    :param d_threshold: Threshold for the distance between two points
    :param perp_angle_thresh: Maximum angle for two points
    :return: Returns the best 4 points that forms the maximum rectangle in our Jigsaw Piece
    """

    N = len(pts)

    distances = cdist(pts, pts)
    distances[distances < distance_threshold] = 0

    angles = compute_list_of_angles(pts)
    possible_rectangles = []

    def traverse_for_possible_rectangle(index, prev_points=[]):
        """
        This function is a huge recursive method to traverse throughout our input list and tries combinations
        with applied angle logic to find likely rectangle fits, will return the best rectangle found in these traverses

        :param index: Current rectangle point
        :param prev_points: All other points traversed before hand
        :return: The best 4 points of any rectangle (The maximum rectangle found)
        """
        curr_point = pts[index]
        depth = len(prev_points)

        # Take the first input point of the first corner of a rectangle
        if depth == 0:
            right_points_index = np.nonzero(np.logical_and(pts[:, 0] > curr_point[0], distances[index] > 0))[0]

            for right_point_idx in right_points_index:
                traverse_for_possible_rectangle(right_point_idx, [index])

            return

        last_angle = angles[index, prev_points[-1]]
        perpendicular_angle = last_angle - 90

        # No negative angles
        if perpendicular_angle < 0:
            perpendicular_angle += 180

        # Depth at 1 means we select another input point, and recursively try other point at depth 2, to see if these
        # lines will form right angles, if not we don't take those 2 points
        if depth in (1, 2):
            # Calculate the Angle degrees and see if they are between our threshold
            diff0 = np.abs(angles[index] - perpendicular_angle) <= perpendicular_angle_threshold
            diff180_0 = np.abs(angles[index] - (perpendicular_angle + 180)) <= perpendicular_angle_threshold
            diff180_1 = np.abs(angles[index] - (perpendicular_angle - 180)) <= perpendicular_angle_threshold
            angle_diffs = np.logical_or(diff0, np.logical_or(diff180_0, diff180_1))

            explore_pts = np.nonzero(np.logical_and(angle_diffs, distances[index] > 0))[0]

            # We look for all the other points to be traversed, with good angles between the threshold
            for explore_index in explore_pts:
                next_points = prev_points[::]
                next_points.append(index)

                traverse_for_possible_rectangle(explore_index, next_points)

        # if a valid rectangle is found, add to list (4 * 90 degree like angles) is found,
        if depth == 3:
            angle_41 = angles[index, prev_points[0]]
            # Calculate the Angle degrees and see if they are between our threshold
            diff0 = np.abs(angle_41 - perpendicular_angle) <= perpendicular_angle_threshold
            diff180_0 = np.abs(angle_41 - (perpendicular_angle + 180)) <= perpendicular_angle_threshold
            diff180_1 = np.abs(angle_41 - (perpendicular_angle - 180)) <= perpendicular_angle_threshold
            dist = distances[index, prev_points[0]] > 0

            if dist and (diff0 or diff180_0 or diff180_1):
                rectangle_points = prev_points[::]
                rectangle_points.append(index)

                already_present = False
                for possible_rectangle in possible_rectangles:
                    if set(possible_rectangle) == set(rectangle_points):
                        already_present = True
                        break

                if not already_present:
                    possible_rectangles.append(rectangle_points)

    [traverse_for_possible_rectangle(i) for i in range(N)]

    # We now have a List of possible rectangles and the angles between all points
    # We now calculate a best fit point system for it by taking the area of the rectangle * norm of likely rectangles
    area_of_rectangles = []
    likely_rectangular = []  # A List that stores all the likely rectangles
    diff_angles = []

    # Loop through all possible rectangles and calculate the area then the best fit points
    for rectangle in possible_rectangles:
        points = pts[rectangle]
        area_of_rectangles.append(polygon_area(points[:, 0], points[:, 1]))

        angle_percent = 0
        diff_angles2 = []

        # For each 3 points of a rectangle, we computer the angles between them
        for pt1, pt2, pt3 in [(0, 1, 2), (1, 2, 3), (2, 3, 0), (3, 0, 1)]:
            diff_angle = abs(angles[rectangle[pt1], rectangle[pt2]] - angles[rectangle[pt2], rectangle[pt3]])
            diff_angles2.append(abs(diff_angle - 90))
            angle_percent += (diff_angle - 90) ** 2

        diff_angles.append(diff_angles2)
        likely_rectangular.append(angle_percent)

    # We turn the Python Lists into a NumPy array and then compute the area * gaussian norm of a rectangle being "real"
    best_fits = np.array(area_of_rectangles) * norm(0, 150).pdf(np.array(likely_rectangular))
    maximum_rectangle_index = possible_rectangles[np.argmax(best_fits)]  # Location of the best fit rectangle is the best one

    return pts[maximum_rectangle_index]
