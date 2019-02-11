import cv2
import json
from find_line_in_image import find_line_contour
from find_parameters_by_coordinates import measure_distance, measure_angle


def init():
    global cap
    global points_dictionary
    cap = cv2.VideoCapture(1)
    points_dictionary = {
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0}
    }


def get_data():
    ret, frame = cap.read()
    line_contour = find_line_contour(frame)
    cv2.imshow("image", frame)
    cv2.waitKey(1)
    output = frame
    if line_contour is None:
        points_dictionary["found"] = False
        points_dictionary["p1"]["d"] = 0
        points_dictionary["p1"]["a"] = 0
        points_dictionary["p2"]["d"] = 0
        points_dictionary["p2"]["a"] = 0
    if line_contour is not None:
        points_dictionary["found"] = True
        max_bottom_box_point = [0, 0]
        second_max_bottom_box_point = [0, 0]
        for x, y in line_contour:
            if y > max_bottom_box_point[1]:
                if y >= max_bottom_box_point[1]:
                    second_max_bottom_box_point = max_bottom_box_point
                    max_bottom_box_point = (x, y)
                else:
                    second_max_bottom_box_point = y
        y = (max_bottom_box_point[1] + second_max_bottom_box_point[1]) / 2
        x = (max_bottom_box_point[0] + second_max_bottom_box_point[0]) / 2
        points_dictionary["p1"]["d"] = measure_distance(
            y, x, frame.shape, 38.5, 28, 20
            )
        points_dictionary["p1"]["a"] = measure_angle(x, frame.shape, 20)
        output = cv2.drawContours(
            output, [line_contour],
            -1, (0, 0, 255), 4
        )
    cv2.imshow("output", output)
    return json.dumps(points_dictionary).encode('utf-8')
