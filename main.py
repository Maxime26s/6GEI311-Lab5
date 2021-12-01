# pip install -r requirements.txt 
import tkinter
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
class Options(tk.Toplevel):
    def __init__(self, parent):
        #super().__init__(parent)  # no need it
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0)

        self.threshold = ""
        self.framerate = ""
        self.compression_ratio = ""
        self.scale_ratio = ""
        self.kernel_size = ""
        self.bg_buffer_size = ""
        self.motion_buffer_size = ""

        self.option = tkinter.Toplevel()
        self.option.geometry("+1000+600")
        self.option.title("Options")
        self.tab = ttk.Notebook(self.option)  # Création du système d'onglets
        self.t1 = ttk.Frame(self.tab)  
        self.t2 = ttk.Frame(self.tab)  
        self.t3 = ttk.Frame(self.tab)
        self.t4 = ttk.Frame(self.tab) 
        self.t5 = ttk.Frame(self.tab)
        self.tab.add(self.t1, text="General") 
        self.tab.add(self.t2, text="Resize")
        self.tab.add(self.t3, text="Gaussian blur")  
        self.tab.add(self.t4, text="Bg buffer")
        self.tab.add(self.t5, text="Motion buffer")
        self.tab.pack(expand=1, fill="both")

        self.add_tab1()
        self.add_tab2()
        self.add_tab3()
        self.add_tab4()
        self.add_tab5()

    def confirm_options(self):
        pass

    def add_tab1(self):
        self.l0 = Label(self.t1, text="Threshold", anchor="w")
        self.l0.grid(row=0, column=0, padx=10, pady=(15,10))

        self.ent0 = Entry(self.t1, textvariable=self.threshold, width=21)  # font=(,'Terminal',30))
        self.ent0.place(width=150, height=50)
        self.ent0.grid(row=0, column=1, pady=5, padx=10)

        self.l1 = Label(self.t1, text="Framerate", anchor="w")
        self.l1.grid(row=1, column=0, padx=10, pady=10)

        self.ent1 = Entry(self.t1, textvariable=self.framerate, width=21)  # font=(,'Terminal',30))
        self.ent1.place(width=150, height=50)
        self.ent1.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t1, text="Confirm", padx=24)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    def add_tab2(self):
        vlist = ["CV2"]

        self.l1 = Label(self.t2, text="Algorithme", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15,10))

        self.combo = ttk.Combobox(self.t2, values = vlist)
        self.combo.set("Pick an algo")
        self.combo.grid(row=0, column=1,padx = 5, pady = 5)

        self.l1 = Label(self.t2, text="Scale ratio", anchor="w")
        self.l1.grid(row=1, column=0, padx=10, pady=(15,10))

        self.ent2 = Entry(self.t2, textvariable=self.scale_ratio, width=21)  # font=(,'Terminal',30))
        self.ent2.place(width=150, height=50)
        self.ent2.grid(row=1, column=1, pady=5, padx=10)

        self.l2 = Label(self.t2, text="Compression", anchor="w")
        self.l2.grid(row=2, column=0, padx=10, pady=10)

        self.ent3 = Entry(self.t2, textvariable=self.compression_ratio, width=21)  # font=(,'Terminal',30))
        self.ent3.place(width=150, height=50)
        self.ent3.grid(row=2, column=1, pady=5, padx=10)

        button = Button(self.t2, text="Confirm", padx=24)
        button.grid(row=3, columnspan=2, padx=5, pady=5)

    def add_tab3(self):
        vlist = ["CV2"]

        self.l1 = Label(self.t3, text="Algorithme", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15,10))

        self.combo = ttk.Combobox(self.t3, values = vlist)
        self.combo.set("Pick an algo")
        self.combo.grid(row=0, column=1,padx = 5, pady = 5)

        self.l2 = Label(self.t3, text="Kernel size", anchor="w")
        self.l2.grid(row=1, column=0, padx=10, pady=(15,10))

        self.ent4 = Entry(self.t3, textvariable=self.kernel_size, width=21)  # font=(,'Terminal',30))
        self.ent4.place(width=150, height=50)
        self.ent4.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t3, text="Confirm", padx=24)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    def add_tab4(self):
        vlist = ["CV2"]

        self.l1 = Label(self.t4, text="Algorithme", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15,10))

        self.combo = ttk.Combobox(self.t4, values = vlist)
        self.combo.set("Pick an algo")
        self.combo.grid(row=0, column=1,padx = 5, pady = 5)

        self.l2 = Label(self.t4, text="Buffer size", anchor="w")
        self.l2.grid(row=1, column=0, padx=10, pady=(15,10))

        self.ent5 = Entry(self.t4, textvariable=self.bg_buffer_size, width=21)  # font=(,'Terminal',30))
        self.ent5.place(width=150, height=50)
        self.ent5.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t4, text="Confirm", padx=24)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    def add_tab5(self):
        vlist = ["CV2"]

        self.l1 = Label(self.t5, text="Algorithme", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15,10))

        self.combo = ttk.Combobox(self.t5, values = vlist)
        self.combo.set("Pick an algo")
        self.combo.grid(row=0, column=1,padx = 5, pady = 5)

        self.l2 = Label(self.t5, text="Buffer size", anchor="w")
        self.l2.grid(row=1, column=0, padx=10, pady=(15,10))

        self.ent6 = Entry(self.t5, textvariable=self.motion_buffer_size, width=21)  # font=(,'Terminal',30))
        self.ent6.place(width=150, height=50)
        self.ent6.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t5, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=2, columnspan=2, padx=5, pady=5)


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
            command=partial(self.open_stat),
        )
        button3.grid(row=1, column=2, padx=5, pady=5)

        button4 = Button(
            self,
            text="Options",
            width = 10,
            command=partial(self.open_options),
        )
        button4.grid(row=1, column=3, padx=5, pady=5)

        button5 = Button(
            self,
            text="Help",
            width = 10,
            # command=partial(self.open_help),
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

    def open_stat(self):
        stat = tk.Toplevel()
        stat.geometry("+1000+350")
        stat.title("Statistiques")

    def open_options(self):
        window = Options(self)
        window.grab_set()

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
            # self.frame = self.vs.read()
            self.frame = get_image()
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
