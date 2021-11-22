import cv2
from processing import read_video, clean_dice_video_seq

_video_file_path = r'data\dice_video_1.mp4'


if __name__ == '__main__':

    im_seq_bgr = read_video(_video_file_path)

    im_seq = clean_dice_video_seq(im_seq_bgr)

    for i, frame in enumerate(im_seq):
        frame_bgr = cv2.cvtColor(frame.astype('float32') / 255, cv2.COLOR_RGB2BGR)

        cv2.namedWindow(f'frame {i}')
        cv2.imshow(f'frame {i}', frame_bgr)
        cv2.waitKey(0)
        cv2.destroyWindow(f'frame {i}')