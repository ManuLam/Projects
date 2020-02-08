CANNY_JIGSAW_PATH = 'canny_edge_pieces/'
CANNY_JIGASW_PIECE = 'canny_jigsaw_piece_{}.png'

FULL_IMAGE_CANNY_JIGSAW_PATH = 'full_image_canny_edge_pieces/'
FULL_IMAGE_CANNY_JIGASW_PIECE = 'full_image_canny_jigsaw_piece_{}.png'

NORMAL_JIGSAW_PATH = 'jigsaw_pieces/'
NORMAL_JIGASW_PIECE = 'jigsaw_piece_{}.png'

FULL_JIGSAW_IMAGE = 'full_jigsaw_cropped.png'

ENRICHED_PIECES_PATH = 'enriched_pieces/'
ENRICHED_PIECES = 'enriched_pieces_{}.png'

JIGSAW_PIECES_COUNT = 13
SIDE_PIECES_BOX = []

import os

def setup(folder_names):
    for folder in folder_names:
        if not os.path.exists(folder):
            os.mkdir(folder)


# Runs at setup
setup([CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGSAW_PATH, NORMAL_JIGSAW_PATH, ENRICHED_PIECES_PATH])
