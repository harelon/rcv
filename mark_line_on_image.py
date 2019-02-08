import argparse
import cv2
from find_line_in_image import find_line_contour


def mark_rectangle_contour():
    # return the points of the contour the looks most like rectangle
    best_fitting_rectangle = find_line_contour(image)        

    # draws the contour on the lower half of the image
    output = cv2.drawContours(
        image, best_fitting_rectangle,
        -1, (0, 0, 255), 4
    )

    cv2.imshow("output", output)
    # show the marked best fitting rectangle if there is one


def args_parser():
    global image
    parser = argparse.ArgumentParser(
            description='An image white line will be detected in'
            )
    # we need a parser
    # to run the program from command line and select one of the photos we took

    parser.add_argument(
            'image',
            help='the path of the image'
        )
    # we need an image path argument to know on what to apply the program

    args = parser.parse_args()
    # convert the arguments into something we can use

    image_path = args.image
    # reads the args image paramater into image_path

    image = cv2.imread(image_path)
    # read the image from the path we are given


def main():
    args_parser()
    mark_rectangle_contour()
    # wait for key press then destroy all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
