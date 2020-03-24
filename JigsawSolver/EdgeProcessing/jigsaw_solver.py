# Takes in array of Jigsaw pieces
# Uses logic on sides / edges
import math

import cv2
from PIL import Image, ImageDraw
from JigsawPiece import JigsawPiece
from global_config import ENRICHED_PIECES_PATH, ENRICHED_PIECE, JIGSAW_PIECES_COUNT, NORMAL_JIGSAW_PATH, \
    NORMAL_JIGASW_PIECE
from harrisCorner import harris_corner_with_rotation
from jigsaw_visualizer import find_max_edge_size, n_piece_splitter, template_maker, template_piece_swapper


def jisaw_array(Jigsaw_List, show=False):
    corner_pieces = find_corners(Jigsaw_List)

    if show:
        for piece in corner_pieces:
            cv2.imshow('tst', cv2.imread(piece.image_file))
            cv2.waitKey(0)

    side_pieces = find_sides(Jigsaw_List)

    if show:
        for side_piece in side_pieces:
            cv2.imshow('tst', cv2.imread(side_piece.image_file))
            cv2.waitKey(0)

    for corner_piece in corner_pieces:
        corner_piece.print_side_info()
        cv2.imshow('tst', cv2.imread(corner_piece.image_file))
        cv2.waitKey(0)
        find_match(corner_piece, side_pieces)


    # for start in corner_pieces:
    # #     # Start with a Corner piece, try fit another corner, then sides, find all the sides and corners
    # #     1


    #return templated_jigsaw


def find_corners(Jigsaw_List):
    return [piece for piece in Jigsaw_List if piece.STRAIGHT_SIDE_COUNT == 2]


def find_sides(Jigsaw_List):
    return [piece for piece in Jigsaw_List if piece.STRAIGHT_SIDE_COUNT == 1]


def find_match(piece1, other_pieces):
    # Compare_inner_with_outter()
    # Check 4 sides.\
    piece1_sides = piece1.get_sides()
    corner_tuple = piece1.get_corner_tuple()

    for side in piece1_sides:
        side_type = side['edge_type']
        if side_type != 'FLAT':
            for p2 in other_pieces:
                p2_sides = p2.get_sides()
                for s2 in p2_sides:
                    found = comparator(p2, side, s2, corner_tuple)
                    if found != 0:
                        cv2.imshow('Piece', cv2.imread(p2.image_file))
                        cv2.imshow('Side', s2['pixels'])

                        cv2.waitKey(0)


reverse_sides = {'IN': 'OUT', 'OUT': 'IN'}
LEFT_SIDE_ARRAY = ['BOT', 'RIGHT', 'TOP', 'LEFT'] # -
RIGHT_SIDE_ARRAY = ['LEFT', 'BOT', 'RIGHT', 'TOP'] # +


# Method for comparing 2 sides and their other sides
def comparator(piece, p1, p2, corner_tuple):
    # (corner_tuple, search_side)
    right_rotation = [(('BOT', 'LEFT'), 'RIGHT'), (('BOT', 'RIGHT'), 'TOP'), (('LEFT', 'TOP'), 'BOT'), (('RIGHT', 'TOP'), 'LEFT')]
    left_rotation = [(('BOT', 'LEFT'), 'TOP'), (('BOT', 'RIGHT'), 'LEFT'), (('LEFT', 'TOP'), 'RIGHT'), (('RIGHT', 'TOP'), 'BOT')]
    # Corner tuple, search side

    if p2['edge_type'] == reverse_sides[p1['edge_type']]:
        if (corner_tuple, p1['side']) in left_rotation:
            if piece.get_side(LEFT_SIDE_ARRAY[LEFT_SIDE_ARRAY.index(p2['side']) - 1])['edge_type'] == 'FLAT':
                print('corner tuple {} side {} left rotation'.format(corner_tuple, p1['side']))
                return p1

        elif(corner_tuple, p1['side']) in right_rotation:
            if piece.get_side(RIGHT_SIDE_ARRAY[(RIGHT_SIDE_ARRAY.index(p2['side']) + 1) % 4])['edge_type'] == 'FLAT':
                print('corner tuple {} side {} right rotation'.format(corner_tuple, p1['side']))
                return p1


    return 0

    # What type of Corner do we have?? If we have it in these two sets, we can determine which side to look at for a FLAT
    # L, B -  R   p2.outer/inner.[LEFT] == 'FLAT' | L, B -  T   p2.outer/inner.[RIGHT] == 'FLAT'
    # L, T -  B   p2.outer/inner.[LEFT] == 'FLAT' | L, T -  R   p2.outer/inner.[RIGHT] == 'FLAT'
    # R, B -  T   p2.outer/inner.[LEFT] == 'FLAT' | R, B -  L   p2.outer/inner.[RIGHT] == 'FLAT'
    # R, T -  L   p2.outer/inner.[LEFT] == 'FLAT' | R, T -  B   p2.outer/inner.[RIGHT] == 'FLAT'


N = 4
placed_array = [0] * N  # 0 | 1
N = 4

pieces = [ENRICHED_PIECES_PATH + ENRICHED_PIECE.format(i) for i in range(JIGSAW_PIECES_COUNT)]
pieces2 = [NORMAL_JIGSAW_PATH + NORMAL_JIGASW_PIECE.format(i) for i in range(JIGSAW_PIECES_COUNT)]

max_w, max_h = find_max_edge_size(pieces)

seperated_pieces = n_piece_splitter(N, pieces)
seperated_pieces2 = n_piece_splitter(N, pieces2)


# logic of right side fits = array[r+1][c]
# logic of left side fits = array[r-1][c]
# logic of top side fits = array[r][c-1]
# logic of bot side fits = array[r][c+1]


# Creates a jigsaw template based on the pieces from 0 -> N size
template_maker(N, max_w, max_h, seperated_pieces, save='canvas.png', show=False)
template_maker(N, max_w, max_h, seperated_pieces2, save='canvas2.png', show=False)

# Allows us to swap 2 elements and update the jigsaw template
template_piece_swapper(N, max_w, max_h, seperated_pieces, 'canvas.png', piece1=ENRICHED_PIECES_PATH + ENRICHED_PIECE.format(0), piece2=ENRICHED_PIECES_PATH + ENRICHED_PIECE.format(1), show=False)
template_piece_swapper(N, max_w, max_h, seperated_pieces2, save='canvas2.png', piece1=NORMAL_JIGSAW_PATH + NORMAL_JIGASW_PIECE.format(5), piece2=NORMAL_JIGSAW_PATH + NORMAL_JIGASW_PIECE.format(1), show=False)

# Currently based on DIR of enriched images, will be using returned Harris Corner pieces for our solution

# Template maker, creates a fresh template at the start, then traverses the array to find pieces
jigsaw_pieces = harris_corner_with_rotation(show=False)
jisaw_array(jigsaw_pieces)
