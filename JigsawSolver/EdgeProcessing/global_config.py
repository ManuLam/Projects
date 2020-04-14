"""
A Setup module

#1 All Folder DIR are kept here
#2 Ran at setup, to ensure all DIR are created
"""

import os

FULL_JIGSAW_IMAGE = 'full_jigsaw_cropped.png'

ORIGINAL_JIGSAW_PATH = 'jigsaw_pieces/'
ORIGINAL_JIGASW_PIECE = 'jigsaw_piece_{}.png'

ROTATED_ORIGINAL_PIECES_PATH = 'rotated_jigsaw_pieces/'
ROTATED_ORIGINAL_CANNY_PIECES = 'rotated_jigsaw_piece_{}.png'

FILTERED_JUNK_PATH = 'junk_pieces/'
JUNK_PIECES = 'junk_pieces_{}.png'

CANNY_JIGSAW_PATH = 'canny_edge_pieces/'
CANNY_JIGASW_PIECE = 'canny_jigsaw_piece_{}.png'

FULL_IMAGE_CANNY_JIGSAW_PATH = 'full_image_canny_edge_pieces/'
FULL_IMAGE_CANNY_JIGASW_PIECE = 'full_image_canny_jigsaw_piece_{}.png'

ROTATED_CANNY_PIECES_PATH = 'rotated_canny_pieces/'
ROTATED_CANNY_PIECES = 'rotated_canny_pieces_{}.png'

HARRIS_PIECES_PATH = 'harris_pieces/'
HARRIS_PIECES = 'harris_pieces_{}.png'

HOUGHP_PIECES_PATH = 'hough_pieces/'
HOUGHP_SIDE_PIECES_PATH = 'side/'
HOUGHP_NON_SIDE_PIECES_PATH = 'non_side/'
HOUGHP_PIECES = 'hough_pieces_{}.png'

CLASSIFICATION_PATH = 'four_side_classifier_pieces/'
CLASSIFICATION_PIECE = 'four_side_classifier_pieces_{}.png'

ENRICHED_EDGE_CLASSIFIER_PIECES_PATH = 'enriched_edges_pieces/'
ENRICHED_EDGE_CLASSIFIER_PIECE = 'enriched_edges_pieces_{}.png'

ENRICHED_INNER_OUTER_PIECES_PATH = 'enriched_inner_outer_pieces/'
ENRICHED_INNER_OUTER_PIECE = 'enriched_inner_outer_pieces_{}.png'

JIGSAW_PIECES_COUNT = 11
SIDE_PIECES_BOX = []

colours = {'AQUA': (255, 255, 0), 'GREEN': (0, 255, 0), 'BLUE': (255, 0, 0),
           'RED': (0, 0, 255), 'ORANGE': (0, 165, 255), 'WHITE': (255, 255, 255)}


def setup(folder_names):
    for folder in folder_names:
        if not os.path.exists(folder):
            os.mkdir(folder)


# Runs at setup
setup([CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGSAW_PATH, ORIGINAL_JIGSAW_PATH, ENRICHED_EDGE_CLASSIFIER_PIECES_PATH,
       ROTATED_ORIGINAL_PIECES_PATH, ROTATED_CANNY_PIECES_PATH, HARRIS_PIECES_PATH, FILTERED_JUNK_PATH,
       HOUGHP_PIECES_PATH, HOUGHP_PIECES_PATH + HOUGHP_SIDE_PIECES_PATH, HOUGHP_PIECES_PATH + HOUGHP_NON_SIDE_PIECES_PATH,
       CLASSIFICATION_PATH, ENRICHED_INNER_OUTER_PIECES_PATH])


