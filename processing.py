import cv2
import numpy as np
from skimage import morphology


def read_video(file_path: str) -> np.ndarray:

    cap = cv2.VideoCapture(file_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_buffer = np.empty((frame_count, frame_height, frame_width, 3), np.dtype('uint8'))

    for fr in range(frame_count):
        ret, frame_buffer[fr] = cap.read()
        if not ret:
            break

    cap.release()

    return frame_buffer


def clean_dice_video_seq(im_seq: np.ndarray) -> np.ndarray:

    # Convert the bgr image sequence to rgb
    im_seq_rgb = np.empty(im_seq.shape)
    for i, frame in enumerate(im_seq):
        im_seq_rgb[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Normalize the brightness to remove shadows
    # im_seq_rgb_norm = np.empty(im_seq_bgr.shape)
    # for i, frame in enumerate(im_seq_rgb):
    #     denom = np.sum(im_seq_rgb[i], axis=2)
    #     im_seq_rgb_norm[i] = np.divide(im_seq_rgb[i], denom[..., np.newaxis], where=(denom[..., np.newaxis] != 0))

    # Define upper and lower RGB bounds for background color
    lower_green = np.array([0, 50, 0])
    upper_green = np.array([200, 255, 100])

    # Remove green background
    im_seq_rgb_no_bg = np.copy(im_seq_rgb)
    for i, frame in enumerate(im_seq_rgb):
        mask = cv2.inRange(frame, lower_green, upper_green)
        im_seq_rgb_no_bg[i][mask != 0] = [255, 0, 0]

    # Remove small regions
    threshold = 100.
    im_seq_rgb_mask = np.zeros(im_seq_rgb.shape[0:3], dtype=bool)
    for i, frame in enumerate(im_seq_rgb_no_bg):
        mask = np.sum(frame, axis=2) > threshold
        im_seq_rgb_mask[i][mask] = True

    obj_min_size = 100
    im_seq_rgb_clean_mask = np.empty(im_seq_rgb_mask.shape, dtype=bool)
    for i, dirty_mask in enumerate(im_seq_rgb_mask):
        im_seq_rgb_clean_mask[i] = morphology.remove_small_objects(dirty_mask, min_size=obj_min_size)
        im_seq_rgb_clean_mask[i] = morphology.closing(im_seq_rgb_clean_mask[i])

    # im_seq_rgb_clean = np.copy(im_seq_rgb_no_bg)
    # for i, mask in enumerate(im_seq_rgb_clean_mask):
    #     im_seq_rgb_clean[i][mask == 0] = [0, 0, 0]

    return np.array(im_seq_rgb_clean_mask, dtype=int) * 255
