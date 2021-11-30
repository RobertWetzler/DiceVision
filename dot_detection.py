import cv2


REGION_MIN_SIZE = 20

def dfs(img, x, y, label, region_stats):
    img[y, x] = label + 1
    region_stats[label]['x_sum'] += x
    region_stats[label]['y_sum'] += y
    region_stats[label]['count'] += 1
    if y > 0 and img[y - 1, x] == 0:
        dfs(img, x, y - 1, label, region_stats)
    if x > 0 and img[y, x - 1] == 0:
        dfs(img, x - 1, y, label, region_stats)
    if y < img.shape[0] - 1 and img[y + 1, x] == 0:
        dfs(img, x, y + 1, label, region_stats)
    if x < img.shape[1] - 1 and img[y, x + 1] == 0:
        dfs(img, x + 1, y, label, region_stats)


def connected_components(img):
    """
    Finds and labels dots in img using recursive connected components. Returns stats of each region. Note that dots
    are given a label in the image one greater than their label in the stats dictionary.
    :param img: The binary image to find and label dots on
    :return: The number of labels and a dictionary of stats for each region (x_sum, y_sum, count, and mean_pos).
    """
    y_max, x_max = img.shape
    label = 0
    region_stats = {}
    for y in range(0, y_max):
        for x in range(0, x_max):
            if img[y, x] == 0:
                label += 1
                region_stats[label] = {'x_sum': 0, 'y_sum': 0, 'count': 0}
                dfs(img, x, y, label, region_stats)
                x_mean = int(region_stats[label]['x_sum'] / region_stats[label]['count'])
                y_mean = int(region_stats[label]['y_sum'] / region_stats[label]['count'])
                region_stats[label]['center'] = (x_mean, y_mean)
                if region_stats[label]['count'] < REGION_MIN_SIZE: #remove small regions
                    del region_stats[label]
    return label, region_stats


def detect_face(img):
    img = cv2.cvtColor(img.astype('float32'), cv2.COLOR_BGR2GRAY)
    num_dots, dot_stats = connected_components(img)
    return num_dots, dot_stats
