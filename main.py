# pip install -r requirements.txt 
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from functools import partial
import math
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from image_processing import ImageProcessing
import cv2
from imutils.video import FileVideoStream, VideoStream
import threading
from time import time
from image_acquisition import get_image
import send_alert


image_processing = ImageProcessing()
# https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays
# Classe contenant l'application (tkinter)

class Interface(tk.Tk):
    # Initialisation de la fenêtre
    def __init__(self):
        self.path = "./camT.mp4"
        tk.Tk.__init__(self)
        self.create_main()
        self.label = None
        self.count = 0
        self.thread = None
        self.last_frame_time = time()
        self.vs = FileVideoStream(self.path).start()
        # self.vs = VideoStream(src=0).start()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

    # Création de boutons
    def create_main(self):
        button1 = Button(
            self,
            text="Source",
            width = 10,
            command=partial(self.select_file),
        )
        button1.grid(row=1, column=0, padx=5, pady=5)

        button2 = Button(
            self,
            text="Motion filter",
            width = 10,
            command=partial(self.open_motiom_filter),
        )
        button2.grid(row=1, column=1, padx=5, pady=5)

        button3 = Button(
            self,
            text="Stats",
            width = 10,
            command=partial(self.video_loop),
        )
        button3.grid(row=1, column=2, padx=5, pady=5)

        button4 = Button(
            self,
            text="Options",
            width = 10,
            command=partial(self.video_loop),
        )
        button4.grid(row=1, column=3, padx=5, pady=5)

        button5 = Button(
            self,
            text="Help",
            width = 10,
            command=partial(self.video_loop),
        )
        button5.grid(row=1, column=4, padx=5, pady=5)


        # self.button_test = tk.Button(self, 
        #                             text="Send email",
        #                             command=partial(send_email))
        # self.button_test.pack(side="bottom")
        

    # Fonction de sélection de fichier
    def select_file(self):
        Tk().withdraw()
        fileName = askopenfilename()
        self.path = fileName
        return

    def open_motiom_filter(self):
        motion_filter = tk.Toplevel()
        motion_filter.geometry("+1000+100")
        motion_filter.title("Motion Filter")

        if self.label is None:
            self.label = tk.Label(motion_filter, image=self.image)
            self.label.grid(row=0, columnspan=5, padx=10,pady=10)
        else:
            self.label.configure(image=self.image)

        self.label.image = self.image
    

    def select_two_images(self):
        self.image1 = np.array(self.select_file("images\IPcam1.png"))
        self.image2 = np.array(self.select_file("images\IPcam2.png"))
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
            # self.frame = get_image()
            if self.frame is None:
                break

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = image_processing.process_image1(image)
            # image = image_processing.resize_cv(image, 1920 / image.shape[1])
            image = Image.fromarray(image_processing.color_movement.astype("uint8"))
            # image = image.resize(
            #    (1920, int((float(image.size[1]) * float((1920 / float(image.size[0]))))))
            # )
            self.display_image(image)

    def display_image(self, image1):
        self.image = ImageTk.PhotoImage(image1)

        if self.label is None:
            self.label = tk.Label(image=self.image)
            self.label.grid(row=0, columnspan=5, padx=10,pady=10)
        else:
            self.label.configure(image=self.image)
        self.label.image = self.image

        self.count += 1

    def resize(self, image):
        size = 1920, 1080
        image.thumbnail(size, Image.ANTIALIAS)
        return image

    # Fonction pour fermer l'application
    def quit(self):
        self.master.destroy()


if __name__ == "__main__":
    root = Interface()
    root.title("Motion detection")
    root.mainloop()
