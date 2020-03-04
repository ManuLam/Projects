import math

import cv2
import numpy as np

#  TopL - TopR
#  TopL - BotL
#  TopR - BotR
#  BotL - BotR
corner_index_pairs = [(0, 1), (0, 3), (1, 2), (2, 3)]  # Order we will create/match lines
corner_index_pairs_colours = [(255,255,0), (0,255,0), (255,0,0), (0,0,255)]  # Colours in this order


def draw_lines_from_corner(img, pts):
    for p1, p2 in corner_index_pairs:
        index = corner_index_pairs.index((p1,p2))
        cv2.line(img, (pts[p1][0], pts[p1][1]), (pts[p2][0], pts[p2][1]), corner_index_pairs_colours[index], thickness=1, lineType=8)


def compute_lines_param(pt1, pt2):
    x0,y0 = pt1[0],pt1[1]
    x1,y1 = pt2[0],pt2[1]
    return y1-y0, x0-x1, x1*y0 - x0*y1


def compute_lines_params(pts):
    return [compute_lines_param(pts[p1], pts[p2]) for p1, p2 in corner_index_pairs]


def point_to_line_dist(x, y, line_params):
    A,B,C = line_params[0], line_params[1], line_params[2]
    return abs((A*x) + (B*y) + C) / math.sqrt(A*A + B*B)


# We go through every pixel in our image and classify which side of the jigsaw it belongs to
# Goal: Extracts 4 sides from jigsaw piece image
def classify_jigsaw_edges(edges, corners, threshold=50, show=False):
    lines = compute_lines_params(corners)
    ys,xs,z = np.nonzero(edges)
    image_classifier = np.zeros(edges.shape)

    d = {1:corner_index_pairs_colours[0],2:corner_index_pairs_colours[1],3:corner_index_pairs_colours[2],4:corner_index_pairs_colours[3]}

    for x, y in zip(xs, ys):
        distance_from_lines = [point_to_line_dist(x, y, line) for line in lines]

        if show:
            cv2.imshow('show', image_classifier)
            cv2.waitKey(1)

        if np.min(distance_from_lines) < threshold:
            image_classifier[y, x] = d[np.argmin(distance_from_lines) + 1]  # Index starts at 0, so add 1
        else:
            print('broken threshold')

    return image_classifier
