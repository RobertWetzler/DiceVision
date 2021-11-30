from cv2 import cv2
import numpy as np
from skimage import morphology
from skimage.morphology import disk

# Define gaussian smoothing kernel
_gauss_kernel3x3 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
_gauss_kernel7x7 = np.array([[1, 3, 7, 9, 7, 3, 1], [3, 12, 26, 33, 26, 12, 3], [7, 26, 55, 70, 55, 26, 7], [9, 33, 70, 90, 70, 33, 9], [7, 26, 55, 70, 55, 26, 7], [3, 12, 26, 33, 26, 12, 3], [1, 3, 7, 9, 7, 3, 1]]) / 1098

# Define dark threshold for normalization
_dark_threshold = 80

# Define upper and lower RGB bounds for background color
_lower_green = np.array([0, 100, 0])  # np.array([0, 50, 0])
_upper_green = np.array([200, 255, 100])

# Define threshold for luminance of dots
_threshold = 100.

# Define minimum object size for dots
_min_obj_size = 20


# Read video file into image sequence given file name
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


# Perform 7x7 Gaussian blur on each image in image sequence
def _gauss_blur(im_seq: np.ndarray) -> np.ndarray:

    im_seq_blur = np.empty(im_seq.shape)
    for i, frame in enumerate(im_seq):
        im_seq_blur[i] = cv2.filter2D(frame, -1, _gauss_kernel7x7)

    return im_seq_blur


# Convert image sequence from bgr to rgb
def _bgr_to_rgb(im_seq: np.ndarray) -> np.ndarray:

    im_seq_rgb = np.empty(im_seq.shape)
    for i, frame in enumerate(im_seq):
        im_seq_rgb[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return im_seq_rgb


# Normalize the luminance of each image in an image sequence, but leaving dark spots dark
def _norm(im_seq: np.ndarray, dark_threshold: int) -> np.ndarray:

    zero_arr = np.zeros((im_seq[0]).shape, dtype=float)

    im_seq_norm = np.empty(im_seq.shape)
    for i, frame in enumerate(im_seq):
        denom = np.sum(im_seq[i], axis=2)
        im_seq_norm[i] = np.divide(im_seq[i], denom[..., np.newaxis], where=(denom[..., np.newaxis] != 0)) * 255
        im_seq_norm[i] = np.where((denom < _dark_threshold)[..., np.newaxis], zero_arr, im_seq_norm[i])

    return im_seq_norm


# Remove the background from each image in the image sequence given another image sequence and boundaries to
# generate masks from
def _rm_bg(im_seq: np.ndarray, im_seq_bg: np.ndarray, bounds: tuple[np.ndarray, np.ndarray]) -> np.ndarray:

    im_seq_no_bg = np.copy(im_seq)
    for i, frame in enumerate(im_seq_bg):
        # mask = cv2.inRange(frame, bounds[0], bounds[1])
        lower_mask = bounds[0][np.newaxis, ...] <= frame
        upper_mask = frame <= bounds[1][np.newaxis, ...]
        mask = np.logical_and(np.all(lower_mask, axis=2), np.all(upper_mask, axis=2))
        im_seq_no_bg[i][mask] = [255, 255, 255]

    return im_seq_no_bg


# Threshold each image in the given image sequence given a threshold
def _thresh_bool(im_seq: np.ndarray, threshold: float) -> np.ndarray:

    im_seq_thresh = np.zeros(im_seq.shape[0:3], dtype=bool)
    for i, frame in enumerate(im_seq):
        mask = np.sum(frame, axis=2) > threshold
        im_seq_thresh[i][mask] = True

    return im_seq_thresh


# Remove all objects below given size in each image in given image sequence
def _rm_small_objs(im_seq: np.ndarray, min_obj_size: float) -> np.ndarray:

    im_seq_clean = np.empty(im_seq.shape, dtype=bool)
    for i, frame in enumerate(im_seq):
        im_seq_clean[i] = np.invert(morphology.remove_small_objects(np.invert(frame), min_size=min_obj_size))

    return im_seq_clean


# Perform a closing on each object (dilation and erosion) in each image in given image sequence
def _close_objs(im_seq: np.ndarray) -> np.ndarray:

    im_seq_closed = np.empty(im_seq.shape, dtype=bool)
    for i, frame in enumerate(im_seq):
        im_seq_closed[i] = np.invert(morphology.closing(np.invert(frame), disk(2, dtype=bool)))

    return im_seq_closed


# Pre-process dice image sequence for detection
def clean_dice_video_seq(im_seq: np.ndarray) -> np.ndarray:

    # Convert the bgr image sequence to rgb
    im_seq_rgb = _bgr_to_rgb(im_seq)

    # Perform gaussian smoothing over image sequence to reduce noise
    im_seq_blur = _gauss_blur(im_seq_rgb)

    # Normalize the brightness to remove shadows
    im_seq_norm = _norm(im_seq_blur, _dark_threshold)

    # Remove green background
    bounds = (_lower_green, _upper_green)
    im_seq_no_bg = _rm_bg(im_seq_rgb, im_seq_norm, bounds)

    # Threshold
    im_seq_thresh = _thresh_bool(im_seq_no_bg, _threshold)

    # Remove small regions
    im_seq_clean = _rm_small_objs(im_seq_thresh, _min_obj_size)

    # Dilate and erode regions (closing)
    im_seq_closed = _close_objs(im_seq_clean)

    return np.array(im_seq_closed, dtype=int) * 255
