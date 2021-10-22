import cv2 as cv
import numpy as np

haystack_img = cv.imread('league.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('slice2.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

threshold = 0.95

# the np.where() return the values below threshold
locations = np.where(result >= threshold)
# we can zip those up into position tuples
locations = list(zip(*locations[::-1]))

if locations:
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        cv.rectangle(haystack_img, top_left,
                     bottom_right, line_color, line_type)

    cv.imshow("Matches", haystack_img)
    cv.waitKey()

else:
    print('not match!')
