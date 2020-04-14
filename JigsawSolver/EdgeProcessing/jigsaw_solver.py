import cv2
import numpy as np
from global_config import colours
from harris_corner import harris_corner_with_rotation


def solve_jisaw_array(jigsaw_list, show=False):
    """
    This function loops through the entire Jigsaw Pieces list and tries to solve it

    :param jigsaw_list: A List of Jigsaw Pieces to be solved
    :param show: A boolean that can show the progress of our work
    """

    corner_pieces = find_corners(jigsaw_list)  # Finding all the Corner Jigsaw Pieces

    if show:
        for piece in corner_pieces:
            cv2.imshow('tst', cv2.imread(piece.image_file))
            cv2.waitKey(0)  # Waits until user input a keystroke

    side_pieces = find_sides(jigsaw_list)  # Finding all the Side Jigsaw Pieces

    if show:
        for side_piece in side_pieces:
            cv2.imshow('tst', cv2.imread(side_piece.image_file))
            cv2.waitKey(0)  # Waits until user input a keystroke

    for corner_piece in corner_pieces:
        corner_piece.print_side_info()
        cv2.imshow('tst', cv2.imread(corner_piece.image_file))
        cv2.waitKey(0)  # Waits until user input a keystroke

        find_match(corner_piece, side_pieces)


def find_corners(jigsaw_list):
    return [piece for piece in jigsaw_list if piece.STRAIGHT_SIDE_COUNT == 2]


def find_sides(jigsaw_list):
    return [piece for piece in jigsaw_list if piece.STRAIGHT_SIDE_COUNT == 1]


def find_match(piece1, other_pieces):
    """
    This functions looks at a Jigsaw piece and finds the best match for it

    :param piece1:  The first piece to be matched with another
    :param other_pieces: All other pieces that can be matched with this piece
    :return: Best piece that fits
    """

    piece1_sides = piece1.get_sides()
    corner_tuple = piece1.get_corner_tuple()

    # Loop through our Corner piece and the other side pieces for matches
    for side in piece1_sides:
        side_type = side['edge_type']
        if side_type != 'FLAT':
            possible_fits = []
            for piece2 in other_pieces:
                if not piece2.placed:  # If piece2 isn't fitted yet, we work with it
                    p2_sides = piece2.get_sides()
                    for side2 in p2_sides:
                        found = comparator(piece2, side, side2, corner_tuple)
                        if found != 0:
                            possible_fits.append((piece2, side2))
                            cv2.imshow('Piece2', cv2.imread(piece2.image_file))
                            cv2.imshow('Piece1_highlighted', highlight_matching_side(piece1, side))
                            cv2.imshow('Piece2_highlighted', highlight_matching_side(piece2, side2))

                            cv2.waitKey(0)

            if len(possible_fits) > 0:
                print("best fit: ", match_module(side, possible_fits)) # This is the Matching module that wasn't finished


reverse_sides = {'IN': 'OUT', 'OUT': 'IN'}
LEFT_SIDE_ARRAY = ['BOT', 'RIGHT', 'TOP', 'LEFT']  # - shift
RIGHT_SIDE_ARRAY = ['LEFT', 'BOT', 'RIGHT', 'TOP']  # + shift


def comparator(piece1, piece1_side, piece2, corner_tuple):
    """
    This function compares two Jigsaw Side Pieces and then compares their other sides to see if they fit

    :param piece1: Input of the first Jigsaw Piece (Corner piece)
    :param piece1_side: Input of the first Jigsaw Piece's side
    :param piece2: Input of the second Jigsaw Piece
    :param corner_tuple: The location of where this Corner piece is
    :return: 0 if no pieces are matched, else return the side of match
    """

    # (corner_tuple, search_side)
    # Below is logic to define which side we should be looking, An example would be, we have a Top Left corner piece and
    # we want to match the right side, This setup is (('LEFT', 'TOP'), 'RIGHT'), therefore we look in the Right neighbour side of
    # the flat edge on any side piece
    right_rotation = [(('BOT', 'LEFT'), 'RIGHT'), (('BOT', 'RIGHT'), 'TOP'), (('LEFT', 'TOP'), 'BOT'), (('RIGHT', 'TOP'), 'LEFT')]
    left_rotation = [(('BOT', 'LEFT'), 'TOP'), (('BOT', 'RIGHT'), 'LEFT'), (('LEFT', 'TOP'), 'RIGHT'), (('RIGHT', 'TOP'), 'BOT')]

    # If the Edge is the same (FLAT/FLAT) or Opposite (Inner/Outer we check the Left and Right rotations)
    # This rotates the Shift array and allows us to know which side we should be looking for
    if piece2['edge_type'] == reverse_sides[piece1_side['edge_type']]:
        if (corner_tuple, piece1_side['side']) in left_rotation:
            if piece1.get_side(LEFT_SIDE_ARRAY[LEFT_SIDE_ARRAY.index(piece2['side']) - 1])['edge_type'] == 'FLAT':
                print('corner tuple {} side {} left rotation'.format(corner_tuple, piece1_side['side']))
                return piece1_side

        elif(corner_tuple, piece1_side['side']) in right_rotation:
            if piece1.get_side(RIGHT_SIDE_ARRAY[(RIGHT_SIDE_ARRAY.index(piece2['side']) + 1) % 4])['edge_type'] == 'FLAT':
                print('corner tuple {} side {} right rotation'.format(corner_tuple, piece1_side['side']))
                return piece1_side

    return 0


def highlight_matching_side(piece, side):
    """
    This function takes in an image of a piece and the side it should highlight

    :param piece: Input piece image
    :param side: Side of the piece to highlight
    :return: An updated image of the piece with the highlighted side
    """

    h, w, _ = cv2.imread(piece.image_file).shape
    temp_image = 'temp_side_image2.png'
    template_image = np.zeros((h, w, 3), np.uint8)

    highlight_side1 = piece.get_side(side['side'])

    # Loop through all 4 sides (Bottom/Left/Right/Top)
    for side in piece.get_sides():
        cv2.imwrite(temp_image, side['pixels'])
        side_image = cv2.imread(temp_image)

        ys,xs,z = np.nonzero(side_image)
        image_classifier = np.zeros(side_image.shape, np.uint8)

        # If its the same side, highlight with colour else white
        if side == highlight_side1:
            for x, y in zip(xs, ys):
                image_classifier[y, x] = colours['ORANGE']
        else:
            for x, y in zip(xs, ys):
                image_classifier[y, x] = colours['WHITE']

        dst = cv2.addWeighted(template_image, 1, image_classifier, 1, 0.0)
        template_image = dst

    return template_image


# Takes a  and all other possible fits and computes the best fit
# def fit_percentage_array(possible_fits):
#     percent_array = [(piece1.image_file, side['side']) for piece1, side in possible_fits]
#
#     [match_module(piece1.get_side(side['side'])) for piece1, side in possible_fits]  # returns fit percent
#     {piece1 : [POSSIBLE_FITS]}
#     return percent_array


def match_module(side, piece_list):
    """
    This function did not work well, as I would be stopping the Matching Phase here.
    This function takes a list of Jigsaw pieces and single piece, compare them and returns the best fit
    :param piece_list:
    :return: The piece with the best fit
    """
    def compare_images(image_present, image_to_find, color, threshold, show):
        img_present, img_to_find = image_present, image_to_find
        result = cv2.matchTemplate(img_to_find, img_present, cv2.TM_SQDIFF_NORMED)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        loc = np.where(result <= threshold)

        allPts = set()

        if mn <= threshold:
            MPx, MPy = mnLoc  # Extract the coordinates of our best match

            # Step 2: Get the size of the template. This is the same size as the match.
            trows, tcols = img_to_find.shape[:2]
            # Step 3: Draw the rectangle on large_image
            cv2.rectangle(img_present, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 255, 0), 1)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_present, pt, (pt[0] + trows, pt[1] + tcols), color, 1)
            allPts.add((pt[0], pt[1], pt[0] + trows, pt[1] + tcols))

        if show:
            # Display the original image with the rectangle around the match.
            print(image_to_find, mn, threshold)  # print the difference (0-1) to find common threshold
            try:
                cv2.imshow('output', img_present)

                # The image is only displayed if we call this
                cv2.waitKey(0)
            except:
                1

    # returns best fit
    for x in piece_list:
        try:
            compare_images(side['pixels'], x[1]['pixels'], color=(255, 0, 255), threshold=.8, show=True)
        except:
            pass



# # Currently based on DIR of enriched images, will be using returned Harris Corner pieces for our solution
#
# # Template maker, creates a fresh template at the start, then traverses the array to find pieces


jigsaw_pieces = harris_corner_with_rotation(show=True)
solve_jisaw_array(jigsaw_pieces, show=False)
