import os

import image_slicer


# Saves tiles to a DIR with a format of (1, 1), (1, 2)
# If save is disabled, returns an array of split tiles without saving
from JigsawSolver.main import PATH


def image_splitter(solved_jigsaw_image, unsolved_jigsaw_image, n_pieces, save=False):
    tiles = image_slicer.slice(solved_jigsaw_image, n_pieces, save=False)

    if save is True:
        new_directory = PATH + unsolved_jigsaw_image[:-4]

        if not os.path.exists(new_directory):
            os.mkdir(new_directory)

        image_slicer.save_tiles(tiles, directory=new_directory, prefix='slice', format='png')

    return tiles
