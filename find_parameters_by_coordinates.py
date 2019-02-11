import constants
import math


def measure_distance(
    y, x, picture_shape, camera_height, y_leaning_angle, x_turning_pixels,
    z_rotating_angle=0
):

    rotated_x = (
        (x-320) * math.cos(
            math.radians(z_rotating_angle)
            ) + (y - 240) * math.sin(
            math.radians(z_rotating_angle)
            )
        )
    rotated_y = (
        -(x-320) * math.sin(
            math.radians(z_rotating_angle)
            ) + (y - 240) * math.cos(
            math.radians(z_rotating_angle)
            )
        )
    height, width, _ = picture_shape
    y_center = height / 2
    # the center x for the calculations is not really the center pixel
    x_center = int(width / 2) - x_turning_pixels

    dy = -rotated_y
    dx = abs(rotated_x)

    # every angle is the angle the camera is leaned to
    # and the angle calculated by the pixels
    y_diviation_degree = (
        float(y_leaning_angle) + (
            float(dy) / float(constants.Y_PIXELS_PER_DEGREE[height])
            )
        )
    x_diviation_degree = (
        float(dx) / float(constants.X_PIXELS_PER_DEGREE[width])
    )

    # calculating distance from camera base to (x_center, y)
    d_to_x_center_y = camera_height/math.tan(math.radians(y_diviation_degree))

    # calculating distance from camera base to (x,y)
    d_to_x_y = d_to_x_center_y / math.cos(math.radians(x_diviation_degree))
    # return it to the function who called it
    return d_to_x_y


def measure_angle(x, picture_shape, x_turning_pixels):
    _, width, _ = picture_shape

    x_center = int(width / 2) - x_turning_pixels

    # the center x for the calculations is not really the center pixel
    dx = x - x_center

    # and the angle calculated by the pixels
    x_diviation_degree = (float(dx) / float(
        constants.X_PIXELS_PER_DEGREE[width])
        )

    return x_diviation_degree
