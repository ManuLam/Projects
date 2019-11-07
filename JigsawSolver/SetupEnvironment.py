import os

from main import PATH


def setup():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
