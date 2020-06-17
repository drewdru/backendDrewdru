import cv2
import numpy as np
from scipy.signal import find_peaks, medfilt


def lines_segmentation(image):
    invert = 255 - image
    ## (5) find and draw the upper and lower boundary of each lines
    hist = cv2.reduce(invert, 1, cv2.REDUCE_AVG).reshape(-1)

    th = 2
    H, W = invert.shape[:2]
    uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
    lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]

    lines = zip(uppers, lowers)
    for line in lines:
        yield invert[line[0] : line[1]]


def word_segmentation(image):
    median = medfilt(image, 5)

    # apply some dilation and erosion to join the gaps
    thresh = cv2.dilate(median, None, iterations=10)
    thresh = cv2.erode(thresh, None, iterations=10)

    proj = np.sum(thresh, 0)

    is_word = False
    words = []
    for index, value in enumerate(proj):
        if value > 0 and not is_word:
            is_word = True
            words.append(index)
        if is_word and value == 0:
            is_word = False
            words.append(index)

    for row in np.split(image, words, 1)[1:-1:2]:
        yield row


def character_segmentation(image):
    # TODO: apply some dilation and erosion to join the gaps? fixing blur could help
    # TODO: if this doesn't help than try to segmentate by histogram peaks
    contours, hierarchy = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    coord = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if h < 15 or w < 15:
            # TODO: get spechial characters (. , - ' ' "")
            continue
        coord.append((x, y, w, h))
    coord.sort(key=lambda tup: tup[0])

    # cv2.imshow("image", image)
    for cor in coord:
        [x, y, w, h] = cor
        character = image[y : y + h, x : x + w]
        yield character
