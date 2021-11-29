from tkinter.constants import X

import numpy as np


class Motion_Detection:
    def __init__(self, step=1, min_size=1):
        self.step = step
        self.min_size = min_size

    def find_boxes(self, image):
        boxes = []
        y = 0
        x = 0
        while y < image.shape[0]:
            while x < image.shape[1]:
                for box in boxes:
                    if box.contains(x, y):
                        x = box.p2.x + 1
                        break
                if x < image.shape[1]:
                    if image[y][x] >= 127:
                        value = image[y][x]
                        box = self.find_box(image, x, y)
                        if box.size() >= self.min_size:
                            boxes.append(box)
                x += 1
            x = 0
            y += 1
        return boxes

    def find_box(self, image, x, y):
        box = Box(Point(x, y))
        box = self.find_neighbors(image, box, x, y, True)
        box = self.find_neighbors(image, box, x, y, False)
        return box

    def find_neighbors(self, image, box, x, y, left):
        # if x < image.shape[0] - 1 and y < image.shape[1] - 1:
        # arr = np.array(
        #    [
        #        [
        #            image[x - self.step, y - self.step],
        #            image[x, y - self.step],
        #            image[x + self.step, y - self.step],
        #        ],
        #        [image[x - self.step, y], image[x, y], image[x + self.step, y]],
        #        [
        #            image[x - self.step, y + self.step],
        #            image[x, y + self.step],
        #            image[x + self.step, y + self.step],
        #        ],
        #    ]
        # )
        # print(arr)

        if left:
            if box.check_point(image, x - self.step, y - self.step):
                box = self.find_neighbors(
                    image, box, x - self.step, y - self.step, True
                )
            else:
                if box.check_point(image, x - self.step, y):
                    box = self.find_neighbors(image, box, x - self.step, y, True)
                if box.check_point(image, x, y - self.step):
                    box = self.find_neighbors(image, box, x, y - self.step, True)
        else:
            if box.check_point(image, x + self.step, y + self.step):
                box = self.find_neighbors(
                    image, box, x + self.step, y + self.step, False
                )
            else:
                if box.check_point(image, x + self.step, y):
                    box = self.find_neighbors(image, box, x + self.step, y, False)
                if box.check_point(image, x, y + self.step):
                    box = self.find_neighbors(image, box, x, y + self.step, False)
        return box


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Box:
    def __init__(self, p1, p2=Point(0, 0)):
        self.p1 = p1
        self.p2 = p2

    def check_point(self, image, x, y):
        size = image.shape
        # value = image[x][y]
        if x >= 0 and x < size[1] and y >= 0 and y < size[0] and image[y][x] == 127:
            self.p1.x = min(self.p1.x, x)
            self.p1.y = min(self.p1.y, y)
            self.p2.x = max(self.p2.x, x)
            self.p2.y = max(self.p2.y, y)
            return True
        return False

    def size(self):
        return (self.p2.x - self.p1.x) * (self.p2.y - self.p1.y)

    def contains(self, x, y):
        if x >= self.p1.x and x <= self.p2.x:
            if y >= self.p1.y and y <= self.p2.y:
                return True
        return False


def max(a, b):
    if a >= b:
        return a
    return b


def min(a, b):
    if a <= b:
        return a
    return b


if __name__ == "__main__":
    arr = np.array([[0, 0, 0, 0], [0, 255, 255, 255], [0, 0, 255, 255]])
    print(arr.shape)
    motion_detection = Motion_Detection()
    boxes = motion_detection.find_boxes(arr)
    print(boxes)
