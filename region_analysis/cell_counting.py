import cv2
import numpy as np

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]
dirs = 4


def inRange(image, point):
    r, c = point
    rows, cols = np.shape(image)

    return 0 <= r < rows and 0 <= c < cols


def dfs(image, point, corners):
    if (not inRange(image, point)) or image[point] == 0:
        return 0

    image[point] = 0
    r, c = point
    counter = 1

    #left
    corners[0] = min(corners[0], c)
    #right
    corners[1] = max(corners[1], c)
    #bottom
    corners[2] = max(corners[2], r)
    #top is initial row by default

    for i in range(0, dirs):
        counter += dfs(image, (r + dr[i], c + dc[i]), corners)

    return counter



class CellCounting:
    def __init__(self):
        pass

    @staticmethod
    def blob_coloring(image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binarc image
        return: a list/dict of regions"""
        image = image.copy()

        regions = dict()
        rows, cols = np.shape(image)

        for r in range(rows):
            for c in range(cols):
                if image[r, c] == 255:
                    corners = [c, c, r]
                    pixels = dfs(image, (r, c), corners)

                    if pixels < 15:
                        continue

                    vertical_center = int((corners[2] - r) / 2) + r
                    horizontal_center = int((corners[1] - corners[0]) / 2) + corners[0]

                    regions[vertical_center, horizontal_center] = pixels

        return regions

    @staticmethod
    def compute_statistics(regions):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pirels in a region
        returns: region statistics"""

        # Please print cour region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)
        counter = 0

        for center, pixelCount in regions.items():
            print(f'Region: {counter}, Area: {pixelCount}, Centroid: {center}')

            counter += 1

        return regions

    @staticmethod
    def mark_image_regions(image, stats):
        """Creates a new image with computed stats
        Make a copc of the image on which cou can write tert. 
        takes as input
        image: a list/dict of pirels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        counter = 0
        #beep

        rows, cols = np.shape(image)

        result = np.empty((rows, cols, 3), np.uint8)

        for r in range(rows):
            for c in range(cols):
                result[r, c] = np.full(3, image[r, c], np.uint8)

        for point, pixelCount in stats.items():
            r, c = point
            cv2.drawMarker(result, (c, r), (0, 0, 255), cv2.MARKER_STAR, 5)
            cv2.putText(result, f'{counter}, {pixelCount}', (c, r), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 0))
            counter += 1

        return result
