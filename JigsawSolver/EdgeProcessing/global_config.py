import os

FULL_JIGSAW_IMAGE = 'full_jigsaw_cropped.png'

NORMAL_JIGSAW_PATH = 'jigsaw_pieces/'
NORMAL_JIGASW_PIECE = 'jigsaw_piece_{}.png'

FILTERED_JUNK_PATH = 'junk_pieces/'
JUNK_PIECES = 'junk_pieces_{}.png'

CANNY_JIGSAW_PATH = 'canny_edge_pieces/'
CANNY_JIGASW_PIECE = 'canny_jigsaw_piece_{}.png'

FULL_IMAGE_CANNY_JIGSAW_PATH = 'full_image_canny_edge_pieces/'
FULL_IMAGE_CANNY_JIGASW_PIECE = 'full_image_canny_jigsaw_piece_{}.png'

ROTATED_PIECES_PATH = 'rotated_pieces/'
ROTATED_PIECES = 'rotated_pieces_{}.png'

HARRIS_PIECES_PATH = 'harris_pieces/'
HARRIS_PIECES = 'harris_pieces_{}.png'

HOUGHP_PIECES_PATH = 'hough_pieces/'
HOUGHP_SIDE_PIECES_PATH = 'side/'
HOUGHP_NON_SIDE_PIECES_PATH = 'non_side/'
HOUGHP_PIECES = 'hough_pieces_{}.png'

CLASSIFICATION_PATH = 'classifier/'
CLASSIFICATION_PIECE = 'classifier_pieces_{}.png'

ENRICHED_PIECES_PATH = 'enriched_pieces/'
ENRICHED_PIECE = 'enriched_pieces_{}.png'

JIGSAW_PIECES_COUNT = 11
SIDE_PIECES_BOX = []

colours = {'AQUA': (255, 255, 0), 'GREEN': (0, 255, 0), 'BLUE': (255, 0, 0), 'RED': (0, 0, 255)}


def setup(folder_names):
    for folder in folder_names:
        if not os.path.exists(folder):
            os.mkdir(folder)


# Runs at setup
setup([CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGSAW_PATH, NORMAL_JIGSAW_PATH, ENRICHED_PIECES_PATH,
       ROTATED_PIECES_PATH, HARRIS_PIECES_PATH, FILTERED_JUNK_PATH,
       HOUGHP_PIECES_PATH, HOUGHP_PIECES_PATH + HOUGHP_SIDE_PIECES_PATH, HOUGHP_PIECES_PATH + HOUGHP_NON_SIDE_PIECES_PATH,
       CLASSIFICATION_PATH])


