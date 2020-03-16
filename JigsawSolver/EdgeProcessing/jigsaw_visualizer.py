import cv2
from PIL import Image

from global_config import ENRICHED_PIECES_PATH, ENRICHED_PIECE, JIGSAW_PIECES_COUNT, NORMAL_JIGSAW_PATH, \
    NORMAL_JIGASW_PIECE


# Specific location has location in our template
def template_maker(N, width, height, pieces, save):
    background = Image.new('RGB', (N*width, N*height), 'black')
    background.save(save)
    piece_locations = []

    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            img = Image.open(pieces[i][j])

            background.paste(img, (width*i, height*j))
            background.save(save)

    return piece_locations


# Find largest width and height of extracted pieces
def find_max_edge_size(pieces):
    w, h = 0,0

    for image in pieces:
        image_w, image_h = cv2.imread(image).shape[:2]
        h = max(h, image_h)
        w = max(w, image_w)

    return h,w


# Swap two pieces inside a list
def template_piece_swapper():
    1


# merges all progress stages into one png image
def progress_merger():
    1

# Enhances customer experience from knowing which piece is which during solving steps
def piece_labeler():
    1

# Returns a N*N sized list
def n_piece_splitter(N, pieces):
    return [pieces[i:i + N-1] for i in range(0, len(pieces), N-1)]
