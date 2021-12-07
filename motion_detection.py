from tkinter.constants import X
from skimage import measure
import math
import numpy as np


class Motion_Detection:
    def __init__(self, shouldCombine=True, min_size_ratio=0.001):
        self.shouldCombine = shouldCombine
        self.min_size_ratio = min_size_ratio

    # Trouve les objets en mouvements
    def find_boxes(self, image):
        min = image.size * self.min_size_ratio
        contours = measure.find_contours(image)
        boxes = []
        for contour in contours:
            Xmin = np.min(contour[:, 0])
            Xmax = np.max(contour[:, 0])
            Ymin = np.min(contour[:, 1])
            Ymax = np.max(contour[:, 1])

            box = Box(Point(Xmin, Ymin), Point(Xmax, Ymax))
            boxes.append(box)

        if self.shouldCombine:
            combined = True
            while combined == True:
                combined = False
                for box1 in boxes:
                    if box1 != None:
                        for j, box2 in enumerate(boxes):
                            if (
                                box2 != None
                                and box1 != box2
                                and (
                                    box1.contains(box2.p1.x, box2.p1.y)
                                    or box1.contains(box2.p2.x, box2.p2.y)
                                )
                            ):
                                combined = True
                                box1.p1 = Point(
                                    min_val(box1.p1.x, box2.p1.x),
                                    min_val(box1.p1.y, box2.p1.y),
                                )
                                box1.p2 = Point(
                                    max_val(box1.p2.x, box2.p2.x),
                                    max_val(box1.p2.y, box2.p2.y),
                                )
                                boxes[j] = None

        final_boxes = []
        for box in boxes:
            if box != None and box.size() >= min:
                final_boxes.append(box)

        return final_boxes


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def resize(self, ratio):
        self.x = math.floor(self.x * ratio)
        self.y = math.floor(self.y * ratio)


class Box:
    def __init__(self, p1, p2=Point(0, 0)):
        self.p1 = p1
        self.p2 = p2
        self.used = False

    def check_point(self, image, x, y):
        size = image.shape
        if x >= 0 and x < size[1] and y >= 0 and y < size[0] and image[y][x] == 127:
            self.p1.x = min_val(self.p1.x, x)
            self.p1.y = min_val(self.p1.y, y)
            self.p2.x = max_val(self.p2.x, x)
            self.p2.y = max_val(self.p2.y, y)
            return True
        return False

    def size(self):
        return (self.p2.x - self.p1.x) * (self.p2.y - self.p1.y)

    def contains(self, x, y):
        if x >= self.p1.x and x <= self.p2.x:
            if y >= self.p1.y and y <= self.p2.y:
                return True
        return False

    def resize(self, old, new):
        ratio = new / old
        self.p1.resize(ratio)
        self.p2.resize(ratio)


def max_val(a, b):
    if a >= b:
        return a
    return b


def min_val(a, b):
    if a <= b:
        return a
    return b
