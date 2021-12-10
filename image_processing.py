import numpy as np
from collections import deque
from time import time
import cv2
from scipy.signal import convolve2d
from motion_detection import Motion_Detection
import performance_statistics


class ImageProcessing:
    def __init__(
        self,
        diff_threshold=20,
        scale_ratio=0.2,
        compression_ratio=0.5,
        bg_buffer_size=10,
        motion_buffer_size=2,
        kernel=5,
        gaussian_algo="CV2",
        min_size_ratio=0.001,
        shouldCombine=True,
    ):
        self.diff_threshold = int(diff_threshold)
        self.scale_ratio = float(scale_ratio)
        self.compression_ratio = float(compression_ratio)
        self.kernel = kernel

        self.gaussian_algo = gaussian_algo

        self.min_size_ratio = float(min_size_ratio)
        self.shouldCombine = shouldCombine

        self.bg_buffer_size = int(bg_buffer_size)
        self.motion_buffer_size = int(motion_buffer_size)

        self.bg_buffer = deque(maxlen=bg_buffer_size)
        self.motion_buffer = deque(maxlen=motion_buffer_size)
        self.orig_frames = deque(maxlen=motion_buffer_size)
        self.motion_detection = Motion_Detection(
            shouldCombine=self.shouldCombine, min_size_ratio=self.min_size_ratio
        )
        self.bg_sum = None
        self.color_movement = None
        self.detection = None

        performance_statistics.reset_module()

    # Filtre le mouvement dans l'image
    def process_image(self, image):
        img = image
        a = time()
        img = self.resize_cv(img, self.scale_ratio)
        img = self.gaussian_blur(img)
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

        return image, self.color_movement, self.detection, boxes

    # Filtre gaussien
    def custom_gaussian(self, image):
        img = []
        for d in range(3):
            img.append(
                convolve2d(
                    image[:, :, d],
                    np.ones((self.kernel, self.kernel)) * 1 / (self.kernel ** 2),
                    "same",
                    "symm",
                ),
            )
        im_conv = np.stack(img, axis=2).astype("uint8")
        return im_conv

    # Resize une image selon un coefficient
    def resize_cv(self, image, coefficient):
        return cv2.resize(
            image,
            (int(image.shape[1] * coefficient), int(image.shape[0] * coefficient)),
            cv2.INTER_CUBIC,
        )

    # Applique un filtre gaussien sur une image
    def gaussian_blur(self, image):
        img = image

        # Un kernel doit être plus grand que 0 et impaire
        if self.kernel <= 0:
            self.kernel = 1
        elif self.kernel % 2 == 0:
            self.kernel = self.kernel + 1
        if self.gaussian_algo == "CV2":
            img = cv2.GaussianBlur(img, (self.kernel, self.kernel), 0)
        else:
            img = self.custom_gaussian(img)
        return img

    # Valeur absolue de la soustraction de deux images
    def substract_image(self, img1, img2):
        diff = np.abs(img2 - img1)
        return diff

    # Met l'image en noir et blanc selon le threshold
    def apply_diff_threshold(self, image):
        image[image < self.diff_threshold] = 0
        image[image >= self.diff_threshold] = 255
        return image

    # Met l'image en teinte de gris
    def rgb2gray(self, image):
        return np.mean(image, -1)

    # Ajoute l'image à la queue du background
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

    # Calcule la moyenne des images du background
    def calc_background_average(self):
        return self.bg_sum / len(self.bg_buffer)

    # Calcule la moyenne pondérée des images de mouvements
    def calc_weighted_movement_average(self, movement_shape):
        weighted_sum = np.zeros(movement_shape, dtype="float32")
        i = 0
        total = 0
        for frame in self.motion_buffer:
            i += 1
            total += i
            weighted_sum = weighted_sum + frame * i
        return weighted_sum / total
