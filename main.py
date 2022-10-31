import cv2 as cv


def hsv_to_colour(hsv):  # Function for converting HSV values to colour
    colours = {  # HSV colour ranges
        'white': ([0, 0, 179], [179, 16, 255]),
        'yellow': ([15, 51, 0], [27, 183, 215]),
        'blue': ([79, 135, 104], [112, 255, 255]),
        'green': ([24, 53, 93], [158, 255, 255]),
        'red': ([0, 119, 135], [179, 255, 181]),
        'orange': ([0, 118, 157], [179, 255, 255]),
    }


def detect_square(img_location):
    img = cv.imread(img_location)
    contours = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    min_area = 100
    max_area = 1500
    num = 1
    '''for contour in contours:
        area = cv.contourArea(contour)
        if min_area < area < max_area:
            x, y, w, h = cv.boundingRect(contour)
            ROI = img[y:y + h, x:x + w]
            cv.imwrite(f'ROI_{num}.png', ROI)
            num += 1
    cv.imshow('image', img)
    cv.waitKey(0)'''
    for contour in contours:
        perimeter = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.1 * perimeter, True)
        if len(approx) == 4:
            area = cv.contourArea(contour)
            (x, y, w, h) = cv.boundingRect(approx)

            # Find aspect ratio of boundary rectangle around the countours.
            ratio = w / float(h)

            # Check if contour is close to a square.
            if ratio >= 0.8 and ratio <= 1.2 and w >= 30 and w <= 60 and area / (w * h) > 0.4:
                final_contours.append((x, y, w, h))

        # Return early if we didn't found 9 or more contours.
    if len(final_contours) < 9:
        return []


detect_square('cube.jpg')
