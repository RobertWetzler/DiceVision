from dot_detection import detect_face
from square_detectionKmeans import detect_squares
import cv2
from utility import show_error_window


def dotsInRange(dotCenters, xMin, xMax, yMin, yMax):
    numInRange = 0
    for dotCenter in dotCenters:
        if xMin <= dotCenter[0] <= xMax and yMin <= dotCenter[1] <= yMax:
            numInRange += 1
    return numInRange

def doRest(allDots, frame_bgr, im_seq_bgr, num_dots, i):
    a, b = detect_squares(allDots)
    aStart = (int(a[0]) - 33, int(a[1]) - 33)
    aEnd = (int(a[0]) + 33, int(a[1]) + 33)
    bStart = (int(b[0]) - 33, int(b[1]) - 33)
    bEnd = (int(b[0]) + 33, int(b[1]) + 33)
    firstDie = frame_bgr[aStart[1]:aEnd[1], aStart[0]:aEnd[0]]
    secondDie = frame_bgr[bStart[1]:bEnd[1], bStart[0]:bEnd[0]]
    try:
        numOnFirstDice = dotsInRange(allDots, aStart[0], aEnd[0], aStart[1], aEnd[1])
        numOnSecondDice = dotsInRange(allDots, bStart[0], bEnd[0], bStart[1], bEnd[1])
        # Add the rectangles and text to the image, display it
        cv2.rectangle(im_seq_bgr[i], aStart, aEnd, (0, 0, 0), 2)
        cv2.rectangle(im_seq_bgr[i], bStart, bEnd, (0, 0, 0), 2)
        cv2.putText(im_seq_bgr[i], str(numOnFirstDice), aStart, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(im_seq_bgr[i], str(numOnSecondDice), bStart, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if (numOnFirstDice > 6) or (numOnFirstDice < 1) or (numOnSecondDice > 6) or (numOnSecondDice < 1):
            cv2.putText(im_seq_bgr[i], "ERROR: Dice not settled", (187, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        2)
        window_name = f'frame: {i}, dots in frame: {num_dots}'
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, im_seq_bgr[i])
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        cv2.destroyWindow(window_name)
    except:  # if error, skip frame
        show_error_window(im_seq_bgr, i)
