import logging
import ColoredFormatter

from canny_edge import crop_jigsaw_pieces_from_image
from global_config import FULL_JIGSAW_IMAGE, ROTATED_CANNY_PIECES_PATH, ROTATED_CANNY_PIECES, JIGSAW_PIECES_COUNT, \
    FULL_IMAGE_CANNY_JIGSAW_PATH, FULL_IMAGE_CANNY_JIGASW_PIECE
from harris_corner import harris_corner_with_rotation
from hough_lines_p import locate_straight_sides_list, locate_full_canny_straight_sides
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget


class Button(QWidget):
    def __init__(self):
        super().__init__()

        pieceSplitter = QPushButton('piece splitter', self)
        pieceSplitter.move(30, 5)

        harrisRotation = QPushButton('harris rotation', self)
        harrisRotation.move(100, 5)

        locateSides = QPushButton('locate sides', self)
        locateSides.move(170, 5)

        locateSidesFull = QPushButton('locate canny full sides', self)
        locateSidesFull.move(240, 5)

        pieceSplitter.clicked.connect(self.crop_jigsaw_pieces_from_image)
        harrisRotation.clicked.connect(self.harris_corner_with_rotation)
        locateSides.clicked.connect(self.locate_straight_sides)
        locateSidesFull.clicked.connect(self.locate_full_canny_straight_sides)

        self.setGeometry(0,595,800,50)
        self.setWindowTitle("Interface!")

    # Crop out an entire image by each Jigsaw Piece
    # Provides Canny Edged output and Normal output
    # Also filters out junk pieces
    @staticmethod
    def crop_jigsaw_pieces_from_image():
        crop_jigsaw_pieces_from_image(FULL_JIGSAW_IMAGE, crop_out=True, show=True, save=True)

    # Finds the corners of each Jigsaw Piece and rotates the images to become parallel with our working plane
    # Each Jigsaw piece is stored in a side / non side folder
    @staticmethod
    def harris_corner_with_rotation():
        harris_corner_with_rotation()

    # Apply HoughLines P onto each Rotated Jigsaw piece to find side edges
    @staticmethod
    def locate_straight_sides():
        locate_straight_sides_list([ROTATED_CANNY_PIECES_PATH + ROTATED_CANNY_PIECES.format(image_number) for image_number in range(0, JIGSAW_PIECES_COUNT)])

    # Apply HoughLines P onto Entire canny edged image
    @staticmethod
    def locate_full_canny_straight_sides():
        locate_full_canny_straight_sides([FULL_IMAGE_CANNY_JIGSAW_PATH + FULL_IMAGE_CANNY_JIGASW_PIECE.format(image_number) for image_number in range(0, JIGSAW_PIECES_COUNT)])


logging.setLoggerClass(ColoredFormatter.ColoredLogger)
if __name__ == '__main__':
    # Sides to detail / Enrichment of pieces
    # GREEN = FLAT
    # RED = OUTER
    # BLUE = INNER

    app = QApplication([])
    button = Button()
    button.show()
    app.exec()
