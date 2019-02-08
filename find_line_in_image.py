# the modules we need for finding the distance and angle to the line
import cv2
import numpy as np
import sys


def find_line_contour(image):
    opened_threshold_image = __clean_image(image)
    # finds the contours in the image after open was used on it
    # searching only for external contours
    _, contours, _ = cv2.findContours(
        cleaned_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # save the contour that will be returned after the function is used
    # the best fitting rectangle
    cont = None
    # every difference in the area of the minAreaRect
    # will be smaller then sys.maxsize
    # saves it also to decide which is the best fitting rectangle
    minDiffer = sys.maxsize
    # saves the rectangle that circumscribes the most fitting line shape
    bestBox = None
    found_box = False
    for contour in contours:
        # find the straight rectangle that circumscribes the contour
        rect = cv2.minAreaRect(contour)
        # finds the tilted minArea circumscribing rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # if the box is too small it can't be the line
        if cv2.contourArea(box) <= 200:
            continue
        # the contour its shape is closest to be a rectangle
        # is the one that the ratio of the area of the rectangle
        # circumscribing to it is the smallest can't be smaller than one
        # because in every case it will be bigger then the contour inside
        if cv2.contourArea(box) / cv2.contourArea(contour) < minDiffer:
            # updates to be the smaller ratio
            minDiffer = cv2.contourArea(box) / cv2.contourArea(contour)
            # saves the things we will need to use next
            cont = contour
            bestBox = box
        # if it got to this point
        # it means we have at least one suspect
        # of being the line we are searching for
        found_box = True
    # if we didn't find any box matching our criteria
    if not found_box:
        return
    # return the points that are in the contour
    return [cont]


def __clean_image(image):
    global cleaned_image
    # convert image to grayscale for future processing
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # use threshold to eleminate the darker parts in the image
    # that we are not looking for
    _, threshold_image = cv2.threshold(
        gray_image, 210, 255, cv2.THRESH_BINARY
        )

    # use open on threshold picture
    # to reduce white noise caused by brighter spots in the picture
    kernel = np.ones((5, 5), np.uint8)
    opened_threshold_image = cv2.morphologyEx(
        threshold_image, cv2.MORPH_OPEN, kernel, iterations=1
        )
    cleaned_image = opened_threshold_image
