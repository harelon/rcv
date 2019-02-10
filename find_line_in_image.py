# the modules we need for finding the distance and angle to the line
import cv2
import numpy as np
import sys


def find_line_contour(image):
    cleaned_image = __clean_image(image)
    # finds the contours in the image after open was used on it
    # searching only for external contours
    _, contours, _ = cv2.findContours(
        cleaned_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # save the contour that will be returned after the function is used
    # the best fitting rectangle
    cont = None
    minDiffer = sys.maxsize
    # every difference in the area of the minAreaRect
    # will be smaller then sys.maxsize
    # saves it also to decide which is the best fitting rectangle
    found_box = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= 400 or area >= 5000:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        if not (len(approx) <= 6 and len(approx) >= 4):
            continue
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if cv2.contourArea(box) / cv2.contourArea(contour) < minDiffer:
            cont = box
            found_box = True
            minDiffer = cv2.contourArea(box) / cv2.contourArea(contour)
    # if we didn't find any box matching our criteria
    if not found_box:
        return None
    # return the points that are in the contour
    return cont


def __clean_image(image):
    # convert image to grayscale for future processing
    gray = cv2.cvtColor(
        image[0:image.shape[0], 0:image.shape[1]], cv2.COLOR_BGR2GRAY
        )
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh_opened = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel, iterations=2
        )
    blurred = cv2.GaussianBlur(thresh_opened, (5, 5), 0)
    return blurred
