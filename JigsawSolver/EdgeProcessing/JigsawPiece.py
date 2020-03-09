import cv2
import numpy as np

from compute_sides import point_to_line_dist
from global_config import colours

side_types = ['inner', 'outer', 'flat']

from houghLinesP import locate_straight_side_img


class JigsawPiece:
    image_file = None  # Enriched piece
    placed = False  # Is it placed down?
    bSide, lSide, rSide, tSide = {}, {}, {}, {}  # Inner/Outer/Straight

    STRAIGHT_SIDE_COUNT = 0  # 1 = side piece, 2 = corner
    straight_side_located = 0
    rotation = None  # Rotated piece from original position
    centroid = None
    # If side piece, no need to match to another
    # Inner looks for Outers, Outers look for Inners

    def __init__(self, enriched_image_file, rotation_angle=None, line_params=None, centroid=None, show_enriched=False, show_sides=False):
        self.image_file = enriched_image_file  # 'enriched_pieces/enriched_pieces_0.png'
        self.rotation = rotation_angle
        self.centroid = centroid

        self.bSide = dict(pixels=None, edge_type=None, line_param=line_params[0])
        self.lSide = {'pixels': None, 'edge_type': None, 'line_param': line_params[1]}
        self.rSide = {'pixels': None, 'edge_type': None, 'line_param': line_params[2]}
        self.tSide = dict(pixels=None, edge_type=None, line_param=line_params[3])

        # Extract 4 sides from colour of image
        self.bSide['pixels'] = self.extract_where_colour(colours['AQUA'])  # AQUA
        self.lSide['pixels'] = self.extract_where_colour(colours['GREEN'])  # GREEN
        self.rSide['pixels'] = self.extract_where_colour(colours['BLUE'])  # BLUE
        self.tSide['pixels'] = self.extract_where_colour(colours['RED'])  # RED

        for side in [self.bSide, self.lSide, self.rSide, self.tSide]:
            straight_side_located = locate_straight_side_img(side['pixels'], show=False)  # 0 or 1
            self.STRAIGHT_SIDE_COUNT += straight_side_located
            print("Total amount of sides located : {}".format(straight_side_located))

            # Find out if a side is FLAT | INNER | OUTER
            if straight_side_located > 0:
                side['edge_type'] = 'FLAT'
            else:
                side['edge_type'] = self.inner_or_outer(side)

        print("Amount of Straight edges in image: {}".format(self.STRAIGHT_SIDE_COUNT))

        if show_enriched:
            cv2.imshow('Jigsaw Piece Enriched', cv2.imread(self.image_file))

        if show_sides:
            cv2.imshow('Bottom side', self.bSide['pixels'])
            cv2.imshow('Left side', self.lSide['pixels'])
            cv2.imshow('Right side', self.rSide['pixels'])
            cv2.imshow('Top side', self.tSide['pixels'])
            self.print_side_info()

    def extract_where_colour(self, colour):
        img = cv2.imread(self.image_file)
        mask = cv2.inRange(img, colour, colour)

        return mask

    def get_sides(self):
        return [self.bSide, self.lSide, self.rSide, self.tSide]

    def print_side_info(self):
        print('Bottom side is a {}'.format(self.bSide['edge_type']))
        print('Left side is a {}'.format(self.lSide['edge_type']))
        print('Right side is a {}'.format(self.rSide['edge_type']))
        print('Top side is a {}'.format(self.tSide['edge_type']))

    def inner_or_outer(self, side):
        ys,xs = np.nonzero(side['pixels'])
        line_param = side['line_param']

        distances = np.array([point_to_line_dist(x, y, line_param) for x, y in zip(xs, ys)])
        cx1,cy1 = self.centroid
        centroid_distance = point_to_line_dist(cx1, cy1, line_param)
        sign = centroid_distance * np.mean(distances)  # Centroid distance prevents the signs from flipping

        return 'IN' if sign > 0 else 'OUT'
