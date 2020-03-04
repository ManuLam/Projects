import cv2
import numpy as np

from compute_sides import point_to_line_dist

side_types = ['inner', 'outer', 'flat']

from houghLinesP import locate_straight_side_img

colours = {'AQUA': (255,255,0), 'GREEN': (0,255,0), 'BLUE': (255,0,0), 'RED': (0,0,255)}


class JigsawPiece:
    image_file = None  # Enriched piece
    placed = False  # Is it placed down?
    lSide = {}  # Inner/Outer/Straight
    rSide = {}
    tSide = {}
    bSide = {}
    STRAIGHT_SIDE_COUNT = 0  # 1 = side piece, 2 = corner
    straight_side_located = 0
    rotation = None  # Rotated piece from original position
    # If side piece, no need to match to another
    # Inner looks for Outers, Outers look for Inners

    def __init__(self, enriched_image_file, rotation_angle=None, line_params=None, show=True):
        self.image_file = enriched_image_file  # 'enriched_pieces/enriched_pieces_0.png'
        self.rotation = rotation_angle
        self.lSide = {'pixels': None, 'edge_type': None, 'line_param': line_params[0]}  # Inner/Outer/Straight
        self.rSide = {'pixels': None, 'edge_type': None, 'line_param': line_params[1]}
        self.tSide = {'pixels': None, 'edge_type': None, 'line_param': line_params[2]}
        self.bSide = dict(pixels=None, edge_type=None, line_param=line_params[3])

        # Extract 4 sides from colour of image
        self.lSide['pixels'] = self.extract_where_colour(colours['GREEN'])  # GREEN / Inner / Outer / Straight / Pixels
        self.rSide['pixels'] = self.extract_where_colour(colours['BLUE'])  # BLUE
        self.tSide['pixels'] = self.extract_where_colour(colours['RED'])  # RED
        self.bSide['pixels'] = self.extract_where_colour(colours['AQUA'])  # AQUA

        for side in [self.lSide, self.rSide, self.tSide, self.bSide]:
            straight_side_located = locate_straight_side_img(side['pixels'])  # 0 or 1
            self.STRAIGHT_SIDE_COUNT += straight_side_located
            print("Total amount of sides located : {}".format(straight_side_located))

            # Find out if a side is FLAT | INNER | OUTER
            if straight_side_located > 0:
                side['edge_type'] = 'FLAT'
            else:
                side['edge_type'] = self.inner_or_outer(side)


        print("Amount of Straight edges in image: {}".format(self.STRAIGHT_SIDE_COUNT))

        if show:
            cv2.imshow('Jigsaw Piece Enriched', cv2.imread(self.image_file))
            cv2.imshow('Left side', self.lSide['pixels'])
            cv2.imshow('Right side', self.rSide['pixels'])
            cv2.imshow('Top side', self.tSide['pixels'])
            cv2.imshow('Bottom side', self.bSide['pixels'])
            self.print_side_info()

            cv2.waitKey(0)

    def extract_where_colour(self, colour):
        img = cv2.imread(self.image_file)
        mask = cv2.inRange(img, colour, colour)

        return mask

    def print_side_info(self):
        print('Left side is a {}'.format(self.lSide['edge_type']))
        print('Right side is a {}'.format(self.rSide['edge_type']))
        print('Top side is a {}'.format(self.tSide['edge_type']))
        print('Bottom side is a {}'.format(self.bSide['edge_type']))

    def inner_or_outer(self, side):
        ys,xs = np.nonzero(side['pixels'])
        line_param = side['line_param']
        distances = np.array([point_to_line_dist(x, y, line_param) for x, y in zip(xs, ys)])
        return 'none'
