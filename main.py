from time import sleep

import cv2
from processing import read_video, clean_dice_video_seq
from dot_detection import detect_face
from square_detectionKmeans import detect_squares
from computeFinalImage import doRest
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
        doRest(allDots, frame_bgr, im_seq_bgr, num_dots, i)
