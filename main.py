import numpy as np
import cv2

# for built in webcam
cap = cv2.VideoCapture(0)
# for external webcam
# cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_lower_color_1 = np.array([0, 70, 50])
    red_upper_color_1 = np.array([10, 255, 255])
    red_lower_color_2 = np.array([170, 70, 50])
    red_upper_color_2 = np.array([180, 255, 255])

    red_mask_1 = cv2.inRange(hsv, red_lower_color_1, red_upper_color_1)
    red_mask_2 = cv2.inRange(hsv, red_lower_color_2, red_upper_color_2)

    red_color_boundaries = {
        "1": ([0, 70, 50], [10, 255, 255]),
        "2": ([170, 70, 50], [180, 255, 255]),
    }

    blue_lower_color_1 = np.array([100, 150, 0])
    blue_upper_color_1 = np.array([140, 255, 255])
    blue_mask_1 = cv2.inRange(hsv, blue_lower_color_1, blue_upper_color_1)

    blue_color_boundaries = {
        "1": ([100, 150, 0], [140, 255, 255])
    }
    for red_color_name, (lower, upper) in red_color_boundaries.items():
        if red_mask_1.any() or red_mask_2.any():
            print("Red is present")
    for blue_color_name, (lower, upper) in blue_color_boundaries.items():
        if blue_mask_1.any():
            print("Blue is present")

    # drawing the red and blue contour lines
    red_contours, _ = cv2.findContours(red_mask_1 | red_mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, red_contours, -1, (0, 0, 255), 3)
    blue_contours, _ = cv2.findContours(blue_mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, blue_contours, -1, (255, 0, 0), 3)

    # For red color
    red_result = cv2.bitwise_and(frame, frame, mask=red_mask_1 | red_mask_2)
    blue_result = cv2.bitwise_and(frame, frame, mask=blue_mask_1)

    cv2.imshow('frame', red_result | blue_result)
    cv2.imshow('mask', red_mask_1|red_mask_2|blue_mask_1)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
