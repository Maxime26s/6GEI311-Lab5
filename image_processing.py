import math
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from collections import deque
from time import time
import cv2
from PIL import Image, ImageDraw
from scipy.signal import convolve2d
from skimage import measure
from motion_detection import Motion_Detection, Box, Point
import performance_statistics


class ImageProcessing:
    def __init__(
        self,
        diff_threshold=20,
        scale_ratio=0.2,
        compression_ratio=0.5,
        bg_buffer_size=10,
        motion_buffer_size=2,
    ):
        self.diff_threshold = diff_threshold
        self.scale_ratio = scale_ratio
        self.compression_ratio = compression_ratio

        self.bg_buffer_size = bg_buffer_size
        self.motion_buffer_size = motion_buffer_size

        self.bg_buffer = deque(maxlen=bg_buffer_size)
        self.motion_buffer = deque(maxlen=motion_buffer_size)
        self.orig_frames = deque(maxlen=motion_buffer_size)
        self.motion_detection = Motion_Detection()
        self.bg_sum = None
        self.color_movement = None
        self.detection = None

        performance_statistics.reset_module()

    def testGaussian(self, image):
        img = []
        for d in range(3):
            img.append(
                convolve2d(image[:, :, d], np.ones((5, 5)) * 1 / 25, "same", "symm"),
            )
        im_conv = np.stack(img, axis=2).astype("uint8")
        return im_conv

    def resize_cv(self, image, coefficient):
        return cv2.resize(
            image,
            (int(image.shape[1] * coefficient), int(image.shape[0] * coefficient)),
            cv2.INTER_CUBIC,
        )

    def resize_image_rgb(self, image, coefficient):
        test = np.array(
            Image.fromarray(image).resize(
                (int(image.shape[1] * coefficient), int(image.shape[0] * coefficient))
            )
        )

        h, w, d = image.shape
        mult = math.ceil(1 / coefficient)
        image = (
            image.reshape(
                math.floor(h * coefficient), mult, math.floor(w * coefficient), mult, d
            )
            .max(3)
            .max(1)
        )
        return image

    def resize_image_gray(self, image, coefficient):
        h, w = image.shape
        mult = math.ceil(1 / coefficient)
        return (
            image.reshape(
                1, math.floor(h * coefficient), mult, math.floor(w * coefficient), mult
            )
            .max(4)
            .max(2)
            .max(0)
        )

    def prepare_image(self, image):
        img = image
        img = self.resize_cv(img, self.scale_ratio)
        # img = self.testGaussian(img)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = gaussian_filter(img, sigma)
        return img

    def substract_image(self, img1, img2):
        diff = np.abs(img2 - img1)
        return diff

    def apply_diff_threshold(self, image):
        image[image < self.diff_threshold] = 0
        image[image >= self.diff_threshold] = 255
        return image

    def rgb2gray(self, image):
        return np.mean(image, -1)

    def process_image(self, image):
        a = time()
        img = self.prepare_image(image)
        img_float = img.astype("float32")
        b = time()
        performance_statistics.add_stat("image preparation", b - a)

        a = time()
        self.add_to_background(img_float)
        self.motion_buffer.append(img_float)
        b = time()
        performance_statistics.add_stat("image buffers", b - a)

        a = time()
        background_average = self.calc_background_average()
        b = time()
        performance_statistics.add_stat("background average", b - a)

        a = time()
        movement_average = self.calc_weighted_movement_average(img_float.shape)
        b = time()
        performance_statistics.add_stat("weighted movement average", b - a)

        a = time()
        if len(self.bg_buffer):
            movement = self.substract_image(movement_average, background_average)
        else:
            movement = np.zeros(movement_average.shape)
        self.color_movement = movement
        self.apply_diff_threshold(movement)
        movement = movement.astype("uint8")
        b = time()
        performance_statistics.add_stat("image substraction", b - a)

        a = time()
        movement = self.rgb2gray(movement)
        movement[movement > 0] = 254

        self.detection = self.resize_cv(
            movement,
            self.compression_ratio / self.scale_ratio,
        )

        boxes = self.motion_detection.find_boxes(self.detection)
        b = time()
        performance_statistics.add_stat("motion area detection", b - a)

        return image, movement, self.detection, boxes

    def calc_weighted_movement_average(self, movement_shape):
        weighted_sum = np.zeros(movement_shape, dtype="float32")
        i = 0
        total = 0
        for frame in self.motion_buffer:
            i += 1
            total += i
            weighted_sum = weighted_sum + frame * i
        return weighted_sum / total

    def add_to_background(self, image):
        if len(self.motion_buffer) == self.motion_buffer_size:
            frame = self.motion_buffer[0]
        else:
            frame = image

        if self.bg_sum is None:
            self.bg_sum = np.zeros(frame.shape, dtype="float32")
        elif len(self.bg_buffer) == self.bg_buffer_size:
            self.bg_sum = self.bg_sum - self.bg_buffer[0]

        self.bg_sum = self.bg_sum + frame
        self.bg_buffer.append(frame)

    def calc_background_average(self):
        return self.bg_sum / len(self.bg_buffer)
