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
            boxes = self.combine(boxes)

        final_boxes = []
        for box in boxes:
            if box != None and box.size() >= min:
                final_boxes.append(box)

        return final_boxes

    # Combine les box qui se touchent
    def combine(self, boxes):
        combined = True
        while combined == True:
            combined = False
            for box1 in boxes:
                if box1 != None:
                    for j, box2 in enumerate(boxes):
                        if (
                            box2 != None
                            and box1 != box2
                            and (box1.contains(box2.p1) or box1.contains(box2.p2))
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
        return boxes


# Classe représentant un point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Repositionne le point selon une nouvelle dimension
    def resize(self, ratio):
        self.x = math.floor(self.x * ratio)
        self.y = math.floor(self.y * ratio)


class Box:
    def __init__(self, p1, p2=Point(0, 0)):
        self.p1 = p1
        self.p2 = p2

    # Retourne l'aire de la boite
    def size(self):
        return (self.p2.x - self.p1.x) * (self.p2.y - self.p1.y)

    # Vérifie si un point x,y se trouve dans la boite
    def contains(self, p):
        if p.x >= self.p1.x and p.x <= self.p2.x:
            if p.y >= self.p1.y and p.y <= self.p2.y:
                return True
        return False

    # Redéfinie les coins selon une nouvelle taille
    def resize(self, old, new):
        ratio = new / old
        self.p1.resize(ratio)
        self.p2.resize(ratio)


# Retourne la plus grande valeur
def max_val(a, b):
    if a >= b:
        return a
    return b


# Retourne la plus petite valeur
def min_val(a, b):
    if a <= b:
        return a
    return b
