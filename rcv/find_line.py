import cv2
import numpy as np
import sys
import os
import math
import argparse

cleaned_image = None
line_countour = None
points = None


def line_distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return math.sqrt((x1-x2)**2 + (y1 - y2)**2)


def averge_point(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return(int((x1 + x2)/2), int((y1 + y2)/2))


def show_images(image):
    cv2.imshow("image", image)
    cv2.imshow("cleaned_image", cleaned_image)
    # show image with the rectangle marked,
    # if none found will show regular image
    output = image.copy()
    focus_image = cv2.imread('resources' + os.sep + 'robot_focus.jpg')
    output = cv2.bitwise_and(output, focus_image)
    if line_countour is not None:
        output = cv2.drawContours(
            output, [line_countour],
            -1, (0, 0, 255), 4
        )
        output = cv2.circle(output, points[0], 3, (255, 0, 0), -1)
        output = cv2.circle(output, points[1], 3, (0, 255, 0), -1)
    cv2.imshow("output", output)


def extermum_points(contour):
    min_distance = sys.maxsize
    line_top = (0, 0)
    line_bot = (0, 0)
    for i in range(0, 2):
        dis = line_distance(contour[i], contour[i+1])
        if dis < min_distance:
            min_distance = dis
            line_top = averge_point(contour[i], contour[i + 1])
            line_bot = averge_point(contour[i + 2], contour[(i + 3) % 4])
    if line_top[1] > line_bot[1]:
        line_top, line_bot = line_bot, line_top
    return (line_bot, line_top)


def find_line_contour(image):
    # every center of mass will be closer to what we need then this one
    fitting_mass_center = (0, -sys.maxsize-1)
    # find the contours in the image
    _, contours, _ = cv2.findContours(
        image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    # this is the contour we will return as the best contour
    cont = None
    for c in contours:
        contour_area = cv2.contourArea(c)
        # the contour we are searching for won't be smaller
        # than 340 by our calculations of pix to degree and trigonometric
        # and larger than 2950
        if not (340 <= contour_area <= 2950):
            continue
        # get a parameter for how close the approximated should be
        peri = cv2.arcLength(c, True)
        # get the approximated contour shape for our contour
        # each point of the approximated shape is closer then 2nd argument
        # 0.02 is there because it works better on our videos
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has more then 6 vertexes or less than 4 skip it
        if not(4 <= len(approx) <= 6):
            continue
        # get the circumscribing rectangle
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # get the area of circumscribing rectangle area
        box_area = cv2.contourArea(box)
        # get the moments which will help us find the center of mass
        # of the contour
        M = cv2.moments(approx)
        # calculate x,y coordinate of center
        if M["m00"] != 0:
            cY = int(M["m01"] / M["m00"])
            cX = int(M["m10"] / M["m00"])
        else:
            cY = 0
            cX = 0
        half_x = image.shape[1] / 2
        # if the y of the center of mass of the new contour is bigger
        # it means the contour is closer to us and is probably what we
        # are looking for
        if cY > fitting_mass_center[1]:
            # if the current contour is closer in y and x to the bottom center
            # it is out best fitting countour
            if abs(half_x - cX) < abs(half_x - fitting_mass_center[0]):
                cont = box
                fitting_mass_center = (cX, cY)
            # if the current contour has bigger y then the last one
            # by an amount that matters it is probably what we are
            # looking for
            elif cY - fitting_mass_center[1] > 20:
                cont = box
                fitting_mass_center = (cX, cY)
        # if the contour is closer in x to the center but doesn't have bigger Y
        elif abs(half_x - cX) < abs(half_x - fitting_mass_center[0]):
            # then we check if the difference in Y matters and if it does
            # it is probably what are looking for
            if cY - fitting_mass_center[1] > -20:
                cont = box
                fitting_mass_center = (cX, cY)
    return cont


def clean_image(image):
    # get a gray copy of image
    gray = cv2.cvtColor(
        image[0:image.shape[0], 0:image.shape[1]], cv2.COLOR_BGR2GRAY
        )
    focus_image = cv2.imread(
        'resources' + os.sep + 'robot_focus.jpg', cv2.IMREAD_GRAYSCALE
        )
    focused_image = cv2.bitwise_and(gray, focus_image)
    # use threshold on image
    _, thresh = cv2.threshold(focused_image, 210, 255, cv2.THRESH_BINARY)
    # use open to remove white noise from image
    kernel = np.ones((5, 5), np.uint8)
    thresh_opened = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel, iterations=1
        )
    # blur the image to dull the image
    blurred = cv2.GaussianBlur(thresh_opened, (5, 5), 0)
    return blurred


def do_work(image, show=False):
    global cleaned_image
    global line_countour
    global points
    points = None
    # clean the image
    cleaned_image = clean_image(image)
    # find the best contour in the cleaned image
    line_countour = find_line_contour(cleaned_image)
    if line_countour is not None:
        points = extermum_points(line_countour)
    if(show):
        show_images(image)
    return points


def main():
    # parser to get image path
    parser_description = "detects the white line in an image"
    parser = argparse.ArgumentParser(description=parser_description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--video', type=str,
        help='path of video process'
        )
    group.add_argument(
        '--image', type=str,
        help='path of the image to process'
        )
    parser.add_argument(
        '--show', type=bool, default=False,
        help='show images or not'
        )
    args = parser.parse_args()
    if args.image is not None:
        if not os.path.isfile(args.image):
            print('Please provide a valid path to an image file')
            sys.exit(-1)
        image = cv2.imread(args.image)
        # do work on the image
        do_work(image, args.show)
        if args.show:
            cv2.waitKey(0)
    if args.video is not None:
        if not os.path.isfile(args.video):
            print('Please provide a valid path to a video file')
            sys.exit(-1)
        video = cv2.VideoCapture(args.video)
        video.set(cv2.CAP_PROP_FPS, 1)
        while video.isOpened():
            ret, frame = video.read()
            if cv2.waitKey(int(1000 / 30)) == ord('q') or not ret:
                break
            do_work(frame, True)
        video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
