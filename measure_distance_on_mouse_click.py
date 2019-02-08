import argparse
import cv2
import numpy as np
import os
import sys
from find_parameters_by_coordinates import measure_distance


image_cleared = True
image_orig = None
image_copy = None


def draw_measure_box(x, y):
    global image_copy
    height, width = image_copy.shape[0:2]
    print("***********************************")
    print("camera_height = {}".format(camera_height))
    print("x = {} , y = {}".format(x, y))
    x_center = int(width/2)
    y_center = int(height/2)
    image_copy = cv2.rectangle(
        image_copy, (x_center, y_center), (x, y), (0, 255, 0), 2
        )
    print(
        measure_distance(
            y, x, image_copy.shape, camera_height,
            y_leaning_angle, x_turning_pixels
            )
        )


def mouse_callback(event, x, y, flags, param):
    global image_orig, image_copy, image_cleared
    global marks_updated
    if event == cv2.EVENT_LBUTTONDOWN and image_cleared:
        cv2.circle(image_copy, (x, y), 3, (0, 0, 255), 2)
        draw_measure_box(x, y)
        image_cleared = False
    if event == cv2.EVENT_RBUTTONDOWN and not image_cleared:
        image_copy = np.copy(image_orig)
        height, width = image_copy.shape[0:2]
        cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
                 (0, 0, 0), 1)
        cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
                 (0, 0, 0), 1)
        image_cleared = True


def do_work(img):
    global image_orig, image_copy
    print("img = {}".format(img))
    image_orig = cv2.imread(img)
    image_copy = np.copy(image_orig)
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)
    height, width = image_copy.shape[0:2]
    cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
             (0, 0, 0), 1)
    cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
             (0, 0, 0), 1)

    while True:
        cv2.imshow('Image', image_copy)
        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()


def main():
    global camera_height
    global y_leaning_angle
    global x_turning_pixels
    parser_description = "Performs distance calculation to the x,y where the \
        left mouse was clicked"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--image', type=str, required=True,
                        help='path of the image to process')
    parser.add_argument('--camera-height', type=float, default=38.5,
                        help="the height of camera when the picture was taken")
    parser.add_argument('--y_leaning_angle', type=float, default=28,
                        help="the y angle of camera when the picture was taken"
                        )
    parser.add_argument('--x_turning_pixels', type=float, default=20,
                        help="the difference in pixels between the center line\
                         and a straight reference line\
                         when the picture was taken"
                        )
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    camera_height = args.camera_height
    y_leaning_angle = args.y_leaning_angle
    x_turning_pixels = args.x_turning_pixels
    do_work(args.image)


if __name__ == '__main__':
    main()
