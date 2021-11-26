import cv2
from processing import read_video, clean_dice_video_seq
from dot_detection import detect_face
from square_detectionKmeans import detect_squares
_video_file_path = 'data/dice_video_1.mp4'

if __name__ == '__main__':
    im_seq_bgr = read_video('data/dice_video_1.mp4')

    im_seq = clean_dice_video_seq(im_seq_bgr)
    for i, frame in enumerate(im_seq):
        frame_bgr = cv2.cvtColor(frame.astype('float32') / 255, cv2.COLOR_RGB2BGR)
        num_dots, dot_stats = detect_face(frame_bgr)
        allDots = []
        for dot_label in dot_stats:
            cv2.circle(frame_bgr, dot_stats[dot_label]['center'], radius=0, color=(0, 0, 255), thickness=3)
            allDots.append(dot_stats[dot_label]['center'])
        # a and b are the coordinates of the center of each dice square
        a, b = detect_squares(allDots)
        aStart = (int(a[0]) - 33, int(a[1]) - 33)
        aEnd = (int(a[0]) + 33, int(a[1]) + 33)
        bStart = (int(b[0]) - 33, int(b[1]) - 33)
        bEnd = (int(b[0]) + 33, int(b[1]) + 33)
        firstDie = frame_bgr[aStart[1]:aEnd[1], aStart[0]:aEnd[0]]
        secondDie = frame_bgr[bStart[1]:bEnd[1], bStart[0]:bEnd[0]]
        numOnFirstDice, throwAway1 = detect_face(firstDie)
        numOnSecondDice, throwAway2 = detect_face(secondDie)
        # Add the rectangles and text to the image, display it
        cv2.rectangle(im_seq_bgr[i], aStart, aEnd, (0, 0, 0), 2)
        cv2.rectangle(im_seq_bgr[i], bStart, bEnd, (0, 0, 0), 2)
        cv2.putText(im_seq_bgr[i], str(numOnFirstDice), aStart, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(im_seq_bgr[i], str(numOnSecondDice), bStart, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.namedWindow(f'frame: {i}, dots in frame: {num_dots}')
        cv2.imshow(f'frame: {i}, dots in frame: {num_dots}', im_seq_bgr[i])
        cv2.waitKey(0)
        cv2.destroyWindow(f'frame {i}')
