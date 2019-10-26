import copy

import image_slicer
import random


def piece_joiner(tiles, n_pieces, img_save_name, scramble_jigsaw=True):
    """
    :param tiles: List of tiles with attributes containing an image
    :param n_pieces: Amount of pieces inside our jigsaw puzzle
    :param img_save_name: The name of the newly saved image
    :param scramble_jigsaw: Boolean to scramble the jigsaw or not
    """


    rand_tiles = list(tiles)

    if scramble_jigsaw:
        # Immutable tiles >> transform the tiles in 1,2,3 .. format
        random_order = [i for i in range(n_pieces)]

        random.shuffle(random_order)

        temp = copy.deepcopy(rand_tiles)

        for i in range(n_pieces):
            rand_tiles[i].image = temp[random_order[i]].image

    image = image_slicer.join(tuple(rand_tiles))
    image.save(img_save_name)
