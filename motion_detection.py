DIFF_THRESH = 150


def is_still(img_a, img_b):
    diff = abs((img_a - img_b).sum())
    return diff < DIFF_THRESH
