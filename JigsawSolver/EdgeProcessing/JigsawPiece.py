import cv2
import numpy as np

from compute_sides import point_to_line_dist
from global_config import colours

side_types = ['inner', 'outer', 'flat']

from hough_lines_p import locate_straight_side_img


class JigsawPiece:
    image_file = None  # Enriched piece
    placed = False  # Is it placed
    bSide, lSide, rSide, tSide = {}, {}, {}, {}  # Inner/Outer/Flat types

    STRAIGHT_SIDE_COUNT = 0  # 1 = side piece, 2 = corner
    straight_side_located = 0
    rotation = None  # Rotated piece from original position
    centroid = None

    def __init__(self, enriched_image_file, rotation_angle=None, line_params=None, centroid=None, show_enriched=False, show_sides=False):
        """
        Initialise a Jigsaw Piece Object with information to setup the piece.

        :param enriched_image_file:  The fully enriched image of this Jigsaw piece
        :param rotation_angle:  The rotated angle of the piece
        :param line_params: A list of Line parameters that is used to classify each side as (BOTTOM/LEFT/RIGHT/TOP) and their Edge types
        :param centroid: The geometric center of the Jigsaw piece
        :param show_enriched: To show the progress of our Jigsaw piece
        :param show_sides: To show each side (BOTTOM/LEFT/RIGHT/TOP) of our Jigsaw piece
        """

        self.image_file = enriched_image_file  # 'enriched_edges_pieces/enriched_edges_pieces_0.png.png'
        self.rotation = rotation_angle
        self.centroid = centroid

        self.bSide = dict(side='BOT', pixels=None, edge_type=None, line_param=line_params[0])
        self.lSide = {'side': 'LEFT', 'pixels': None, 'edge_type': None, 'line_param': line_params[1]}
        self.rSide = {'side': 'RIGHT', 'pixels': None, 'edge_type': None, 'line_param': line_params[2]}
        self.tSide = dict(side='TOP', pixels=None, edge_type=None, line_param=line_params[3])

        # Extract 4 sides from colour of image
        self.bSide['pixels'] = self.extract_where_colour(colours['AQUA'])  # AQUA
        self.lSide['pixels'] = self.extract_where_colour(colours['GREEN'])  # GREEN
        self.rSide['pixels'] = self.extract_where_colour(colours['BLUE'])  # BLUE
        self.tSide['pixels'] = self.extract_where_colour(colours['RED'])  # RED

        print('Jigsaw Piece: {}'.format(self.image_file))
        for side in self.get_sides():
            straight_side_located = locate_straight_side_img(side['pixels'], show=False)  # 0 or 1
            self.STRAIGHT_SIDE_COUNT += straight_side_located
            print("Total amount of sides located on {} side : {}".format(side['side'], straight_side_located))

            # Find out if a side is FLAT | INNER | OUTER
            if straight_side_located > 0:
                side['edge_type'] = 'FLAT'
            else:
                side['edge_type'] = self.inner_or_outer(side)

        print("Amount of Straight edges in image: {} \n".format(self.STRAIGHT_SIDE_COUNT))

        if show_enriched:
            cv2.imshow('Jigsaw Piece Enriched', cv2.imread(self.image_file))

        if show_sides:
            cv2.imshow('Bottom side', self.bSide['pixels'])
            cv2.imshow('Left side', self.lSide['pixels'])
            cv2.imshow('Right side', self.rSide['pixels'])
            cv2.imshow('Top side', self.tSide['pixels'])
            self.print_side_info()

    def extract_where_colour(self, colour):
        """
        This function masks out the colour declared by the input parameter

        :param colour: The colour of the pixels we want to extract
        :return: 2D numpy array containing of all the pixels we extracted
        """

        img = cv2.imread(self.image_file)  # Read the image file of this Jigsaw piece
        mask = cv2.inRange(img, colour, colour)

        return mask

    def get_side(self, side):
        """
        This function returns the side of a Jigsaw Piece based off the input parameter

        :param side: The Side of the Jigsaw Piece we want to return
        """

        if side == 'BOT':
            return self.bSide
        elif side == 'LEFT':
            return self.lSide
        elif side == 'RIGHT':
            return self.rSide
        elif side == 'TOP':
            return self.tSide

    def get_sides(self):
        """
        This function returns all the sides of a Jigsaw piece as a List

        :return: [BOTTOM SIDE, LEFT SIDE, RIGHT SIDE, TOP SIDE]
        """

        return [self.bSide, self.lSide, self.rSide, self.tSide]

    def get_corner_tuple(self):
        """
        This function only returns a tuple if the Jigsaw Piece is a Corner Piece with 2 FLAT edges. Example: If the
        current Jigsaw piece is the top left corner piece, it should return (LEFT, TOP).

        :return: (FLAT_SIDE_1, FLAT_SIDE_2) Only returns a tuple of 2 FLAT sides
        """

        return tuple([side['side'] for side in self.get_sides() if side['edge_type'] == 'FLAT'])

    def print_side_info(self):
        """
        This function prints out the edge type for each side in our Jigsaw Piece
        """

        print('Jigsaw Piece: {}'.format(self.image_file))
        print('Bottom side is a {}'.format(self.bSide['edge_type']))
        print('Left side is a {}'.format(self.lSide['edge_type']))
        print('Right side is a {}'.format(self.rSide['edge_type']))
        print('Top side is a {}'.format(self.tSide['edge_type']))

    def inner_or_outer(self, side):
        """
        This function computes the mean of the pixels on a given's side, against the side's classifier line.

        Left/Top sides
            If the mean of the pixels is over the line, it is a Inner. If it falls short of the line it
            is an Outer.

        Right/Bottom sides
            If the mean of the pixels is over the line, it is a Outer. If it falls short of the line it
            is an Inner.

        :param side: side of a Jigsaw piece
        :return: 'IN' or 'OUT' , Defining if a Jigsaw side's edge is an Inner or Outter
        """

        ys, xs = np.nonzero(side['pixels'])  # Pixels extracted
        line_param = side['line_param']  # Line parameters are passed from the side itself

        distances = np.array([point_to_line_dist(x, y, line_param) for x, y in zip(xs, ys)])  # Calculating the distance from each pixel point
        cx1,cy1 = self.centroid
        centroid_distance = point_to_line_dist(cx1, cy1, line_param)
        sign = centroid_distance * np.mean(distances)  # Centroid distance prevents the signs from flipping

        return 'IN' if sign > 0 else 'OUT'

    def set_image_file(self, image_file):
        """
        This function sets the Jigsaw Piece's image path as the input

        :param image_file: Image file name
        """

        self.image_file = image_file
