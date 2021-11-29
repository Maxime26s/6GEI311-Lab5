import numpy as np
import tkinter as tk
import math
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw
from image_processing import ImageProcessing
import cv2
from imutils.video import FileVideoStream, VideoStream
import threading
from time import time

image_processing = ImageProcessing(diff_threshold=20)
# https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays
# Classe contenant l'application (tkinter)
class Application(tk.Frame):
    # Initialisation de la fenêtre
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry("1000x800")
        self.label = None
        self.count = 0
        self.thread = None
        self.last_frame_time = time()
        self.vs = FileVideoStream(path="./camT.mp4").start()
        # self.vs = VideoStream(src=0).start()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

    # Création de boutons
    def create_widgets(self):
        self.selectFile1 = tk.Button(self)
        self.selectFile1["text"] = "Select files"
        self.selectFile1["command"] = self.video_loop
        self.selectFile1.pack(side="top")

    # Fonction de sélection de fichier
    def select_file(self, fileName=""):
        if fileName == "":
            fileName = askopenfilename()
        return Image.open(fileName)

    def select_two_images(self):
        self.image1 = np.array(self.select_file("image1.png"))
        self.image2 = np.array(self.select_file("image2.png"))
        image = Image.fromarray(
            image_processing.process_image(self.image1, self.image2)
        )
        self.display_image(image)

    def video_loop(self):
        while True:
            while time() <= self.last_frame_time + 1 / 30:
                pass
            self.last_frame_time = time()
            self.frame = self.vs.read()
            if self.frame is None:
                break

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image, boxes = image_processing.process_image1(image)
            # image = image_processing.resize_cv(image, 1920 / image.shape[1])
            image = Image.fromarray(image_processing.detection.astype("uint8"))
            # image = image.resize(
            #    (1920, int((float(image.size[1]) * float((1920 / float(image.size[0]))))))
            # )
            for box in boxes:
                image = self.draw_rectangle(image, box)
            self.display_image(image)

    def display_image(self, image1):
        image = ImageTk.PhotoImage(image1)

        if self.label is None:
            self.label = tk.Label(image=image)
            self.label.place(x=0, y=0)
        else:
            self.label.configure(image=image)
        self.label.image = image

        self.count += 1

    def resize(self, image):
        size = 1920, 1080
        image.thumbnail(size, Image.ANTIALIAS)
        return image

    def draw_rectangle(self, image, box):
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (box.p1.y, box.p1.x, box.p2.y, box.p2.x), fill=None, outline="red"
        )
        return image

    # Fonction pour fermer l'application
    def quit(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
