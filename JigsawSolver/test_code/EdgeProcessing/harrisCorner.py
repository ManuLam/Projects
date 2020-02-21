# Apply Harris Corner Algorithm to find maximum rectangle
# Then apply a rotation to the piece, parallel to our wanted plane
import logging

import cv2
import numpy as np

from scipy.stats import norm
from scipy.spatial.distance import cdist
from JigsawSolver.test_code.EdgeProcessing.global_config import CANNY_JIGSAW_PATH, CANNY_JIGASW_PIECE, \
    JIGSAW_PIECES_COUNT, ROTATED_PIECES_PATH, ROTATED_PIECES, HARRIS_PIECES_PATH, HARRIS_PIECES

logger = logging.getLogger(__name__)


# Rotates an image relative to degrees passed
def rotate(image, degrees):
    if len(image.shape) == 3:
        rows, cols, _ = image.shape
    else:
        rows, cols = image.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), degrees, .75)

    return cv2.warpAffine(image, M, (cols, rows)), M


# Find the Corner points per Jigsaw piece, Rotate the image and store the rotated value
def harris_corner_with_rotation():
    for image_number in range(0, JIGSAW_PIECES_COUNT):
        filename = CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE.format(image_number)

        try:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            dst = cv2.cornerHarris(gray, 4, 3, 0.04)

            # result is dilated for marking the corners, not important
            dst = cv2.dilate(dst, None)

            # Threshold for an optimal value, it may vary depending on the image.
            dst_threshold = 0.25
            img[dst > dst_threshold * dst.max()] = [0, 0, 255]

            ret, dst = cv2.threshold(dst, dst_threshold * dst.max(), 255, 0)
            dst = np.uint8(dst)

            try:
                points = find_points(dst, gray)

                intersections = get_best_fitting_rect_coords(points, perp_angle_thresh=30)

                if intersections is None:
                    raise RuntimeError('No rectangle found')

                if intersections[1, 0] == intersections[0, 0]:
                    rotation_angle = 90
                else:
                    rotation_angle = np.arctan2(intersections[1, 1] - intersections[0, 1],
                                                intersections[1, 0] - intersections[0, 0]) * 180 / np.pi

                # Rotate jigsaw image
                rotated_gray, M = rotate(img, rotation_angle)
                logger.info("%s rotated by %d degrees", filename, rotation_angle)

            # Rotate intersection points
                # intersections = np.array(np.round([M.dot((point[0], point[1], 1)) for point in intersections])).astype(np.int)

            except:
                logger.info("No points found for: ", filename)
                pass

            cv2.imwrite(HARRIS_PIECES_PATH + HARRIS_PIECES.format(image_number), img)

            cv2.imwrite(ROTATED_PIECES_PATH + ROTATED_PIECES.format(image_number), rotated_gray)
            cv2.imshow('piece1', img)

            cv2.imshow('piece2', rotated_gray)
            cv2.waitKey(0)

        except:
            logger.info('No corners found for: ', filename, )


def find_points(dst, gray):
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)

    return corners


# Reference to https://towardsdatascience.com/solving-jigsaw-puzzles-with-python-and-opencv-d775ba730660
def get_best_fitting_rect_coords(xy, d_threshold=30, perp_angle_thresh=20, verbose=0):
    """
    Since we expect the 4 puzzle corners to be the corners of a rectangle, here we take
    all detected Harris corners and we find the best corresponding rectangle.
    We perform a recursive search with max depth = 2:
    - At depth 0 we take one of the input point as the first corner of the rectangle
    - At depth 1 we select another input point (with distance from the first point greater
        then d_threshold) as the second point
    - At depth 2 and 3 we take the other points. However, the lines 01-12 and 12-23 should be
        as perpendicular as possible. If the angle formed by these lines is too much far from the
        right angle, we discard the choice.
    - At depth 3, if a valid candidate (4 points that form an almost perpendicular rectangle) is found,
        we add it to the list of candidates.

    Given a list of candidate rectangles, we then select the best one by taking the candidate that maximizes
    the function: area * Gaussian(rectangularness)
    - area: it is the area of the candidate shape. We expect that the puzzle corners will form the maximum area
    - rectangularness: it is the mse of the candidate shape's angles compared to a 90 degree angles. The smaller
                        this value, the most the shape is similar toa rectangle.
    """
    N = len(xy)

    distances = cdist(xy, xy)
    distances[distances < d_threshold] = 0

    def compute_angles(xy):
        angles = np.zeros((N, N))

        for i in range(N):
            for j in range(i + 1, N):

                point_i, point_j = xy[i], xy[j]
                if point_i[0] == point_j[0]:
                    angle = 90
                else:
                    angle = np.arctan2(point_j[1] - point_i[1], point_j[0] - point_i[0]) * 180 / np.pi

                angles[i, j] = angle
                angles[j, i] = angle
        return angles

    angles = compute_angles(xy)
    possible_rectangles = []

    def search_for_possible_rectangle(idx, prev_points=[]):

        curr_point = xy[idx]
        depth = len(prev_points)

        if depth == 0:
            right_points_idx = np.nonzero(np.logical_and(xy[:, 0] > curr_point[0], distances[idx] > 0))[0]

            if verbose >= 2:
                logger.info('point: %s %s ', idx, curr_point)

            for right_point_idx in right_points_idx:
                search_for_possible_rectangle(right_point_idx, [idx])

            return


        last_angle = angles[idx, prev_points[-1]]
        perp_angle = last_angle - 90
        if perp_angle < 0:
            perp_angle += 180

        if depth in (1, 2):
            if verbose >= 2:
                logger.info('%s point: %s , last angle: %s , perp angle: %s ', '\t' * depth, idx, last_angle, perp_angle)

            diff0 = np.abs(angles[idx] - perp_angle) <= perp_angle_thresh
            diff180_0 = np.abs(angles[idx] - (perp_angle + 180)) <= perp_angle_thresh
            diff180_1 = np.abs(angles[idx] - (perp_angle - 180)) <= perp_angle_thresh
            all_diffs = np.logical_or(diff0, np.logical_or(diff180_0, diff180_1))

            diff_to_explore = np.nonzero(np.logical_and(all_diffs, distances[idx] > 0))[0]

            for dte_idx in diff_to_explore:
                if dte_idx not in prev_points: # unlickly to happen but just to be certain
                    next_points = prev_points[::]
                    next_points.append(idx)

                    search_for_possible_rectangle(dte_idx, next_points)


        if depth == 3:
            angle41 = angles[idx, prev_points[0]]

            diff0 = np.abs(angle41 - perp_angle) <= perp_angle_thresh
            diff180_0 = np.abs(angle41 - (perp_angle + 180)) <= perp_angle_thresh
            diff180_1 = np.abs(angle41 - (perp_angle - 180)) <= perp_angle_thresh
            dist = distances[idx, prev_points[0]] > 0

            if dist and (diff0 or diff180_0 or diff180_1):
                rect_points = prev_points[::]
                rect_points.append(idx)

                if verbose == 2:
                    logger.info('We have a rectangle: %s', rect_points)

                already_present = False
                for possible_rectangle in possible_rectangles:
                    if set(possible_rectangle) == set(rect_points):
                        already_present = True
                        break

                if not already_present:
                    possible_rectangles.append(rect_points)

    if verbose >= 2:
        logger.info('Coords: %s', xy)
        logger.info('Distances: %s', distances)
        logger.info('Angles: %s', angles)

    for i in range(N):
        search_for_possible_rectangle(i)

    if len(possible_rectangles) == 0:
        return None

    def PolyArea(x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    areas = []
    rectangularness = []
    diff_angles = []

    for r in possible_rectangles:
        points = xy[r]
        areas.append(PolyArea(points[:, 0], points[:, 1]))

        mse = 0
        da = []
        for i1, i2, i3 in [(0, 1, 2), (1, 2, 3), (2, 3, 0), (3, 0, 1)]:
            diff_angle = abs(angles[r[i1], r[i2]] - angles[r[i2], r[i3]])
            da.append(abs(diff_angle - 90))
            mse += (diff_angle - 90) ** 2

        diff_angles.append(da)
        rectangularness.append(mse)

    areas = np.array(areas)
    rectangularness = np.array(rectangularness)

    scores = areas * norm(0, 150).pdf(rectangularness)
    best_fitting_idxs = possible_rectangles[np.argmax(scores)]
    return xy[best_fitting_idxs]

