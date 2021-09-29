import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color_1 = np.array([0, 70, 50])
    upper_color_1 = np.array([10, 255, 255])
    lower_color_2 = np.array([170, 70, 50])
    upper_color_2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_color_1, upper_color_1)
    mask2 = cv2.inRange(hsv, lower_color_2, upper_color_2)

    color_boundaries = {
        "1": ([0, 70, 50], [10, 255, 255]),
        "2": ([170, 70, 50], [180, 255, 255]),
    }
    for color_name, (lower, upper) in color_boundaries.items():
        if ( mask1.any() or mask2.any() ) == True:
            print("Red is present")

    result = cv2.bitwise_and(frame, frame, mask=mask1|mask2)

    cv2.imshow('frame', result)
    # cv2.imshow('mask', mask1|mask2)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

