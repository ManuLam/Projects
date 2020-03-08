import math

import cv2
import numpy as np
from global_config import colours

corner_index_pairs = {'BOT': (0, 1), 'LEFT': (0, 3), 'RIGHT': (1, 2), 'TOP': (2, 3), }  # Order we will create/match lines
colour_array = [colours['AQUA'], colours['GREEN'], colours['BLUE'], colours['RED']]  # Colours in this order L/R/T/B


def draw_lines_from_corner(img, pts):
    for key in corner_index_pairs.keys():
        p1,p2 = corner_index_pairs[key]
        cv2.line(img, (pts[p1][0], pts[p1][1]), (pts[p2][0], pts[p2][1]),
                 colour_array[list(corner_index_pairs.keys()).index(key)], thickness=1, lineType=8)


def compute_lines_param(pt1, pt2):
    x0,y0 = pt1[0],pt1[1]
    x1,y1 = pt2[0],pt2[1]
    return y1-y0, x0-x1, x1*y0 - x0*y1


def compute_lines_params(pts):
    return [compute_lines_param(pts[p1], pts[p2]) for p1, p2 in corner_index_pairs.values()]


def point_to_line_dist_abs(x, y, line_params):
    A,B,C = line_params[0], line_params[1], line_params[2]
    return abs((A*x) + (B*y) + C) / math.sqrt(A*A + B*B)


def point_to_line_dist(x, y, line_params):
    A,B,C = line_params[0], line_params[1], line_params[2]
    return ((A*x) + (B*y) + C) / math.sqrt(A*A + B*B)


# We go through every pixel in our image and classify which side of the jigsaw it belongs to
# Goal: Extracts 4 sides from jigsaw piece image
def classify_jigsaw_edges(edges, corners, threshold=50, show=False):
    lines = compute_lines_params(corners)
    ys,xs,z = np.nonzero(edges)
    image_classifier = np.zeros(edges.shape)

    for x, y in zip(xs, ys):
        distance_from_lines = [point_to_line_dist_abs(x, y, line) for line in lines]

        if show:
            cv2.imshow('show', image_classifier)
            cv2.waitKey(1)

        if np.min(distance_from_lines) < threshold:
            image_classifier[y, x] = colour_array[np.argmin(distance_from_lines)]  # Index starts at 0, so add 1
        else:
            print('broken threshold')

    return image_classifier
