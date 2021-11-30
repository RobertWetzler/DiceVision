import cv2

def show_error_window(im_seq_bgr, i):
    cv2.putText(im_seq_bgr[i], "ERROR: Dice not settled", (187, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    window_name = f'frame: {i}, ERROR: Dice not Settled'
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, im_seq_bgr[i])
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)
    cv2.destroyWindow(window_name)