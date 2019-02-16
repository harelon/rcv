import argparse
import cv2
from find_line import find_line_contour, clean_image


def mark_rectangle_contour(image):
    # return the points of the contour the looks most like rectangle
    cleaned_image = clean_image(image)
    best_fitting_rectangle = find_line_contour(cleaned_image)
    output = image.copy()
    if best_fitting_rectangle is not None:
        # draws the contour on the lower half of the image
        output = cv2.drawContours(
            image, [best_fitting_rectangle],
            -1, (0, 0, 255), 4
        )
    # show the marked best fitting rectangle if there is one
    return output


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        output = mark_rectangle_contour(frame)
        cv2.imshow("output", output)
        if cv2.waitKey(1) == ord('q'):
            break
    # wait for key press then destroy all windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
