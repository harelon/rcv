import constants
import math


def measure_distance(
    y, x, picture_shape, camera_height, y_leaning_angle, x_turning_pixels
):
    height, width, _ = picture_shape

    y_center = constants.Y_MIDDLE_PIXEL[height]
    x_center = constants.X_MIDDLE_PIXEL[width]

    y_pixels_per_degree = constants.Y_PIXELS_PER_DEGREE[height]
    x_pixels_per_degree = constants.X_PIXELS_PER_DEGREE[width]

    dy = y - y_center
    # the center isn't going to be exactly on the middle pixel
    dx = abs(x - x_center - x_turning_pixels)

    # every angle is the angle the camera is leaned to
    # and the angle calculated by the pixels
    y_diviation_degree = (
        float(y_leaning_angle)+(float(dy)/float(y_pixels_per_degree))
        )
    x_diviation_degree = (float(dx) / float(x_pixels_per_degree))

    # calculating distance from camera base to (x_center, y)
    d_to_x_center_y = camera_height/math.tan(math.radians(y_diviation_degree))
    # calculating distance from camera base to (x,y)
    d_to_x_y = d_to_x_center_y / math.cos(math.radians(x_diviation_degree))
    return d_to_x_y


def measure_angle(x, picture_shape, x_turning_pixels):
    _, width, _ = picture_shape

    x_center = constants.X_MIDDLE_PIXEL[width]

    x_pixels_per_degree = constants.X_PIXELS_PER_DEGREE[width]

    # the center isn't going to be exactly on the middle pixel
    dx = x - x_center - x_turning_pixels

    # and the angle calculated by the pixels
    x_diviation_degree = (float(dx) / float(x_pixels_per_degree))

    return x_diviation_degree
