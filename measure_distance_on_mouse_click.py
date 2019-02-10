import argparse
import cv2
import numpy as np
import os
import sys
import imutils
from find_parameters_by_coordinates import measure_distance


<<<<<<< HEAD
image_cleared = True
image_orig = None
image_copy = None
=======
# GLOBALS #
# the below 2 globals were calculated using  calculate_pixels_per_degree.py utility
X_PIXELS_PER_DEGREE = {
    1280: 24.904907983771232, 640: 12.452453991885616, 320: 6.226226995942808
    }
Y_PIXELS_PER_DEGREE = {
    720: 18.3250528605539775, 480: 12.216701907035985, 240: 6.108350953517992
    }
# 1280 and 720 pixels per degree are derived from the other calculations
image_cleared = True
image_orig = None
image_copy = None
camera_height = 38.5
# udi took photo from the height of 38.5 cm
y_leaning_angle = 24.884483526764288094449822606294
# the camera is leaned by this amount of degrees downwards
# the center of the camera is 83 cm forward
x_turning_angle = 1.9
# the camerais turned by this amount of degrees to the left
# not used but equals to the 35 pixels to the left


class XOrientation(Enum):
    left = -1
    center = 0
    right = 1


class YOrientation(Enum):
    up = -1
    center = 0
    down = 1
>>>>>>> socket_progress


def draw_measure_box(x, y):
    global image_copy

    height, width = image_copy.shape[0:2]
    # seperate from the last distance measured
    print("***********************************")
    print("camera_height = {}".format(camera_height))
    # print the x and y of the point clicked
    print("x = {} , y = {}".format(x, y))
<<<<<<< HEAD
    x_center = int(width/2)
    y_center = int(height/2)
    # draw rectangle on the image from the center to the point clicked
    image_copy = cv2.rectangle(
        image_copy, (x_center, y_center), (x, y), (0, 255, 0), 2
        )
    # print the distance measured by the module
    print(
        measure_distance(
            y, x, image_orig.shape, camera_height,
            y_leaning_angle, x_turning_pixels, z_rotating_angle
            )
        )
=======
    x_center = width/2
    y_center = height/2
    x_pixels_per_degree = X_PIXELS_PER_DEGREE[width]
    y_pixels_per_degree = Y_PIXELS_PER_DEGREE[height]
    print("x_pixels_per_degree = {}".format(x_pixels_per_degree))
    print("y_pixels_per_degree = {}".format(y_pixels_per_degree))
    x_orientation = XOrientation.center
    y_orientation = YOrientation.center
    if x > x_center:
        x_orientation = XOrientation.right
    elif x < x_center:
        x_orientation = XOrientation.left
    if y > y_center:
        y_orientation = YOrientation.down
    elif y < y_center:
        y_orientation = YOrientation.up
    # calculating the quadrants
    o_sum = x_orientation.value + y_orientation.value
    q = -1
    if o_sum == 2:
        q = 4
    elif o_sum == -2:
        q = 2
    elif o_sum == 0:
        if x_orientation.value > y_orientation.value:
            q = 1
        if x_orientation.value < y_orientation.value:
            q = 3
    if q <= 2:
        raise NotImplemented
    # drawing the box
    top_left = None
    bottom_right = None
    if q == 3:
        top_left = (int(x), int(y_center))
        bottom_right = (int(x_center), int(y))
    elif q == 4:
        top_left = (int(x_center), int(y_center))
        bottom_right = (int(x), int(y))
    else:
        raise NotImplemented
    print("top_left = {}".format(top_left))
    print("bottom_right = {}".format(bottom_right))
    image_copy = cv2.rectangle(image_copy, top_left, bottom_right,
                               (0, 255, 0), 2)
    dy = y - y_center
    dx = abs(x - x_center - 35)
    # the center is 35 pixels to the right
    # the center line of the photo is at 675 pixels and not 640
    print("dx = {}".format(dx))
    print("dy = {}".format(dy))
    x_diviation_degree = (float(dx) / float(x_pixels_per_degree))
    y_diviation_degree = (
        float(y_leaning_angle)+(float(dy)/float(y_pixels_per_degree))
        )
    # every angle is the angle the camera is leaned to
    # and the angle calculated by the pixels
    print("x_diviation_degree = {}".format(x_diviation_degree))
    print("y_diviation_degree = {}".format(y_diviation_degree))
    # calculating distance from camera base to (x_center, y)
    d_to_x_center_y = camera_height/math.tan(math.radians(y_diviation_degree))
    # calculating distance from camera base to (x,y)
    d_to_x_y = d_to_x_center_y / math.cos(math.radians(x_diviation_degree))
    print("distance is {}".format(d_to_x_y))
>>>>>>> socket_progress


def mouse_callback(event, x, y, flags, param):
    global image_copy, image_cleared
    # if left was pressed and image is cleared draw a red dot
    if event == cv2.EVENT_LBUTTONDOWN and image_cleared:
        cv2.circle(image_copy, (x, y), 3, (0, 0, 255), 2)
        # call the function that measures the distance to that pixel
        draw_measure_box(x, y)
        # set the image to be not cleared for next time
        image_cleared = False
    # if the right button was clicked and image is not clear, clear it
    if event == cv2.EVENT_RBUTTONDOWN and not image_cleared:
        # copy the image that was clean into image_copy
        image_copy = np.copy(image_orig)
        # draw the same lines from do_work
        height, width = image_copy.shape[0:2]
        cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
                 (0, 0, 0), 1)
        cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
                 (0, 0, 0), 1)
        # set the image to be clean for next time
        image_cleared = True


def do_work(img):
    global image_orig, image_orig, image_copy, original_shape
    print("img = {}".format(img))
    image_orig = cv2.imread(img)    
    image_copy = np.copy(image_orig)
    print(image_copy.shape[0:2])
    cv2.namedWindow('Image')
    # when the mouse is clicked mouse_callback function will be called
    cv2.setMouseCallback('Image', mouse_callback)
    height, width = image_copy.shape[0:2]
    # draw 2 lines to mark that go throught the center of the image
    cv2.line(image_copy, (0, int(height/2)), (int(width), int(height/2)),
             (0, 0, 0), 1)
    cv2.line(image_copy, (int(width/2), 0), (int(width/2), int(height)),
             (0, 0, 0), 1)

    while True:
        cv2.imshow('Image', image_copy)
        k = cv2.waitKey(10)
        # wait until esc is pressed
        if k == 27:
            break
    cv2.destroyAllWindows()


def main():
    global camera_height
    global y_leaning_angle
    global x_turning_pixels
    global z_rotating_angle
    # we need a parser for our program
    parser_description = "Performs distance calculation to the x,y where the \
        left mouse was clicked"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--image', type=str, required=True,
                        help='path of the image to process')
    parser.add_argument('--camera-height', type=float, default=38.5,
<<<<<<< HEAD
                        help="the height of camera when the picture was taken")
    parser.add_argument('--y_leaning_angle', type=float, default=28,
                        help="the y angle of camera when the picture was taken"
                        )
    parser.add_argument('--x_turning_pixels', type=float, default=-20,
                        help="the difference in pixels between the center line\
                         and a straight reference line\
                         when the picture was taken"
                        )
    parser.add_argument('--z_rotating_angle', type=float, default=0,
                        help="the difference in pixels between the center line\
                         and a straight reference line\
                         when the picture was taken"
                        )
    # parse the arguments we were given
=======
                        help="the height of camera when the picture was taken \
                        when the picture was taken")
>>>>>>> socket_progress
    args = parser.parse_args()
    if not os.path.isfile(args.image):
        print('Please provide a valid path to an image file')
        sys.exit(-1)
    # use the arguments we were given
    camera_height = args.camera_height
    y_leaning_angle = args.y_leaning_angle
    x_turning_pixels = args.x_turning_pixels
    z_rotating_angle = args.z_rotating_angle
    do_work(args.image)


if __name__ == '__main__':
    main()
