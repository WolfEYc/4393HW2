import numpy as np


class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        curr = binary_image[0, 0]
        rle = [curr]

        rows, cols = np.shape(binary_image)

        length = 0

        for r in range(rows):
            for c in range(cols):
                length += 1
                if binary_image[r, c] != curr:
                    rle.append(length - 1)
                    curr = binary_image[r, c]
                    length = 1

        if length > 0:
            rle.append(length + 1)

        return rle

    def decode_image(self, rle_code, height, width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        image = np.zeros((height, width), np.uint8)
        counter = 1
        length = rle_code[counter]
        color = rle_code[0]

        for r in range(height):
            for c in range(width):
                image[r, c] = color
                length -= 1
                if length == 0:
                    counter += 1
                    length = rle_code[counter]
                    color = 0 if color == 255 else 255

        return image
