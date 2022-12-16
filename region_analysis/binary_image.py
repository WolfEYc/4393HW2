import numpy as np

threshold = 0


def avg(hist, split, first_section):
    if first_section:
        iterator_range = range(0, split)
    else:
        iterator_range = range(split, len(hist))

    s = 0
    length = 0
    for i in iterator_range:
        s += hist[i] * i
        length += hist[i]

    if length == 0:
        return 0

    return s / length


def weight(hist_split, sum_hist):
    return sum(hist_split) / sum_hist


class BinaryImage:

    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0] * 256

        for r in image:
            for c in r:
                hist[c] += 1

        return hist

    def find_otsu_threshold(self, hist):
        global threshold
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""

        max_variance = 0
        num_pixels = sum(hist)

        for i in range(1, len(hist)):
            firstSplit = hist[:i]
            secondSplit = hist[i:]
            first_weight = weight(firstSplit, num_pixels)
            second_weight = weight(secondSplit, num_pixels)
            first_avg = avg(hist, i, True)
            second_avg = avg(hist, i, False)

            weight_mult = first_weight * second_weight

            curr_variance = weight_mult * pow(first_avg - second_avg, 2)
            if curr_variance > max_variance:
                max_variance = curr_variance
                threshold = i

        return threshold

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: a grey scale image
        returns: a binary image"""


        bin_img = image.copy()
        rows, cols = np.shape(bin_img)

        for r in range(rows):
            for c in range(cols):
                if bin_img[r][c] >= threshold:
                    bin_img[r][c] = 0
                else:
                    bin_img[r][c] = 255

        return bin_img
