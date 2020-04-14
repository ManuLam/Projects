import cv2
from PIL import Image


# Specific location has location in our template
from global_config import JIGSAW_PIECES_COUNT, ORIGINAL_JIGSAW_PATH, ORIGINAL_JIGASW_PIECE, CANNY_JIGSAW_PATH, \
    CANNY_JIGASW_PIECE, HARRIS_PIECES_PATH, HARRIS_PIECES, ROTATED_CANNY_PIECES_PATH, ROTATED_CANNY_PIECES, \
    CLASSIFICATION_PATH, \
    CLASSIFICATION_PIECE, ENRICHED_EDGE_CLASSIFIER_PIECES_PATH, ENRICHED_EDGE_CLASSIFIER_PIECE, \
    ENRICHED_INNER_OUTER_PIECE, \
    ENRICHED_INNER_OUTER_PIECES_PATH, ROTATED_ORIGINAL_PIECES_PATH, ROTATED_ORIGINAL_CANNY_PIECES


def template_maker(N, width, height, pieces, save=None, show=False):
    """
    Takes in parameters and creates a template for all our Jigsaw Pieces to fit into, like a puzzle box

    :param N: The amount of pieces we have
    :param width: The width of the template
    :param height: The height of the template
    :param pieces: A list of pieces to be placed into the template
    :param save:  A boolean to allow us to save the image
    :param show:  A boolean where we can see the progress
    """
    background = Image.new('RGB', (N*width, N*height), 'black')
    background.save(save)

    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            img = Image.open(pieces[i][j])

            background.paste(img, (width*j, height*i))
            background.save(save)

    if show:
        background.show()


# Swap two pieces inside a 2D list, pieces=Jigsaw object
# Make a new image of a "swapped list"
def template_piece_swapper(N, width, height, pieces, save=None, piece1=None, piece2=None, show=False):
    """
    Swap two pieces inside a 2D list, pieces=Jigsaw object
    Make a new image of a "swapped list", shows us the swapping feature of the solver

    :param N: The amount of pieces we have
    :param width: The width of the template
    :param height: The height of the template
    :param pieces: A list of pieces to be placed into the template
    :param save:  A boolean to allow us to save the image
    :param piece1: First piece to be swapped with piece2
    :param piece2: Second piece to be swapped with piece1
    :param show:  A boolean where we can see the progress
    """

    p11,p12 = 0,0
    p21,p22 = 0,0

    for index in range(len(pieces)):
        try:
            if pieces[index].index(piece1):
                p11 = index
                p12 = pieces[index].index(piece1)

        except ValueError:
            pass

        try:
            if pieces[index].index(piece2):
                p21 = index
                p22 = pieces[index].index(piece2)

        except ValueError:
            pass

    pieces[p11][p12], pieces[p21][p22] = piece2, piece1

    template_maker(N, width, height, pieces, save=save, show=show)


# Find largest width and height of extracted pieces
def find_max_edge_size(pieces):
    """
    This function find the largest width and height of any Jigsaw Piece and takes that as the template size

    :param pieces: A list of all Jigsaw pieces
    :return: The maximum width and height of the Jigsaw pieces
    """
    w, h = 0,0

    for image in pieces:
        image_w, image_h = cv2.imread(image).shape[:2]
        h = max(h, image_h)
        w = max(w, image_w)

    return h, w


# Could be ran manually at the end, or a follow up to our automated solution
# merges all progress stages into one png image
def progress_merger():
    """
    This function returns an entire merge of all the steps we have achieved and produced, shows the user
    a template that has all steps from start to finish of enrichment.
    """
    # Full Image
    # ===============
    # Jigsaw pieces
    # Canny Jigsaw pieces
    # Harris Pixel pieces
    # Harris rotated with best 4 points pieces
    # Classified pieces
    # Enriched EDGES classified pieces
    # Enriched INNER OUTER classified pieces

    background = Image.new('RGB', (2300, 1500), 'black')
    background.save('temp.png')

    def pusher(image_path, height_level):
        cumulative_width = 0

        for i in range(JIGSAW_PIECES_COUNT):
            img = Image.open(image_path.format(i))
            background.paste(img, (cumulative_width, 200*height_level))
            background.save('temp_progress_maker.png')
            cumulative_width += width + 10  # A margin gap between two images

    width, height = 0, 0
    for i in range(JIGSAW_PIECES_COUNT):
        img = Image.open(ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE.format(i))
        w, h = img.size

        width, height = max(w, width), max(h, height)

    pusher(ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE, 0)
    pusher(CANNY_JIGSAW_PATH + CANNY_JIGASW_PIECE, 1)
    pusher(HARRIS_PIECES_PATH + HARRIS_PIECES, 2)
    pusher(ROTATED_CANNY_PIECES_PATH + ROTATED_CANNY_PIECES, 3)
    pusher(CLASSIFICATION_PATH + CLASSIFICATION_PIECE, 4)
    pusher(ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE, 5)
    pusher(ENRICHED_INNER_OUTER_PIECES_PATH + ENRICHED_INNER_OUTER_PIECE, 6)

progress_merger()


# Enhances customer experience from knowing which piece is which during solving steps
def piece_labeler():
    1


# Returns a N*N sized list
def n_piece_splitter(N, pieces):
    """
    This function splits the piece in a 2d array MxM

    :param N: The total amount of pieces
    :param pieces: A list of Jigsaw pieces
    :return: The 2d pieces split
    """

    return [pieces[i:i + N-1] for i in range(0, len(pieces), N-1)]


def canvas_merger(image1, image2, save_filename=None):
    """
    This function merges the Enriched canvas and the Original Canvas to show the user the stages of movement

    :param image1: First image to be merged
    :param image2: Second image to be merged
    :param save_filename: The file name to be saved to
    """

    canvas_enriched = Image.open(image1, 'r')
    canvas_original = Image.open(image2, 'r')
    img_w, img_h = canvas_enriched.size

    background = Image.new('RGB', (2*img_w, img_h), 'black')

    background.paste(canvas_enriched, (0, 0))
    background.paste(canvas_original, (img_w, 0))
    background.save(save_filename)


N = 4
placed_array = [0] * N  # 0 | 1
N = 4

pieces = [ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE.format(i) for i in range(JIGSAW_PIECES_COUNT)]
pieces2 = [ROTATED_ORIGINAL_PIECES_PATH + ROTATED_ORIGINAL_CANNY_PIECES.format(i) for i in range(JIGSAW_PIECES_COUNT)]

max_w, max_h = find_max_edge_size(pieces)

separated_pieces = n_piece_splitter(N, pieces)
separated_pieces2 = n_piece_splitter(N, pieces2)


template_maker(N, max_w, max_h, separated_pieces, save='canvas_enriched.png', show=False)
template_maker(N, max_w, max_h, separated_pieces2, save='canvas_original.png', show=False)

# Allows us to swap 2 elements and update the jigsaw template
#template_piece_swapper(N, max_w, max_h, separated_pieces, 'canvas_enriched.png', piece1=ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE.format(0), piece2=ENRICHED_EDGE_CLASSIFIER_PIECES_PATH + ENRICHED_EDGE_CLASSIFIER_PIECE.format(1), show=False)
#template_piece_swapper(N, max_w, max_h, separated_pieces2, save='canvas_original.png', piece1=ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE.format(5), piece2=ORIGINAL_JIGSAW_PATH + ORIGINAL_JIGASW_PIECE.format(1), show=False)

canvas_merger('canvas_enriched.png', 'canvas_original.png', save_filename='canvas.png')
