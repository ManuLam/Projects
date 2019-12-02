import cv2
from matplotlib import pyplot as plt

img = cv2.imread('jigsaw_temp_imgs/2019-10-24-121755.jpg',0)
cannyEdges = cv2.Canny(img, 200, 200)


def cannyOne():
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(122),plt.imshow(cannyEdges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()


cannyOne()

