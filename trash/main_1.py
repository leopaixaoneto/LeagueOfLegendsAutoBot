import cv2 as cv
import numpy as np

haystack_img = cv.imread('league.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('slice.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)


# get the best match position
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

# nota mínima para detectar um sucesso
threshold = 0.8
if max_val >= threshold:
    print("FOUND!")

    # get dimensions of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(haystack_img, top_left, bottom_right, color=(
        0, 255, 0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Result', haystack_img)
    cv.waitKey()

else:
    print("NOT FOUND!")
