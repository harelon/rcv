import cv2
import json
import datetime
from find_line import find_line_contour
from find_parameters_by_coordinates import find_distance_and_angle_by_coordinates


def init():
    global cap
    global points_dictionary
    global last_time            
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    points_dictionary = {
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0}
    }
    last_time = datetime.datetime.now()


def get_data():
    global last_time
    global start_time
    ret, frame = cap.read()
    line_contour = find_line_contour(frame)
    if line_contour is None:
        points_dictionary["found"] = False
        points_dictionary["p1"]["d"] = 0
        points_dictionary["p1"]["a"] = 0
        points_dictionary["p2"]["d"] = 0
        points_dictionary["p2"]["a"] = 0
    if line_contour is not None:
        points_dictionary["found"] = True
        lowest_box_point = [0, 0]
        second_lowest_bottom_box_point = [0, 0]
        highest_box_point = [100000, 100000]
        second_highest_box_point = [100000, 100000]
        for x, y in line_contour:
            if y > second_lowest_bottom_box_point[1]:
                if y >= lowest_box_point[1]:
                    second_lowest_bottom_box_point = lowest_box_point
                    lowest_box_point = (x, y)
                else:
                    second_lowest_bottom_box_point =(x, y)
            if y < second_highest_box_point[1]:
                if y < highest_box_point[1]:
                    second_highest_box_point = highest_box_point
                    highest_box_point = (x,y)
                else:
                    second_highest_box_point = (x,y)
        y1 = (lowest_box_point[1] + second_lowest_bottom_box_point[1]) / 2
        x1 = (lowest_box_point[0] + second_lowest_bottom_box_point[0]) / 2
        d1, a1 = find_distance_and_angle_by_coordinates(
            x1, y1, frame.shape, 38.5, 28, 20
            )
        y2 = (highest_box_point[1] + second_highest_box_point[1]) / 2
        x2 = (highest_box_point[0] + second_highest_box_point[0]) / 2
        d2, a2 = find_distance_and_angle_by_coordinates(
            x2, y2, frame.shape, 38.5, 28, 20
            )
        points_dictionary["p1"]["d"] = d1
        points_dictionary["p1"]["a"] = a1
        points_dictionary["p2"]["d"] = d2
        points_dictionary["p2"]["a"] = a2
    return json.dumps(points_dictionary).encode('utf-8')
