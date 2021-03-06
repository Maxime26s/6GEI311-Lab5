# pip install -r requirements.txt
import tkinter
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
from functools import partial
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw
from image_processing import ImageProcessing
import cv2
from imutils.video import FileVideoStream, VideoStream
import threading
from time import time
from image_acquisition import get_image
import send_alert
import performance_statistics


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


# https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays
# Classe contenant l'application (tkinter)
class Options(tk.Toplevel):
    def __init__(self, parent, oldOptions, confirm):
        # super().__init__(parent)  # no need it
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0)

        self.confirm = confirm

        self.threshold = tk.IntVar(value=20)
        self.framerate = tk.IntVar(value=0)
        self.compression_ratio = tk.DoubleVar(value=0.5)
        self.scale_ratio = tk.DoubleVar(value=0.2)
        self.kernel_size = tk.IntVar(value=5)
        self.bg_buffer_size = tk.IntVar(value=10)
        self.motion_buffer_size = tk.IntVar(value=2)
        self.min_size_ratio = tk.DoubleVar(value=0.001)
        self.shouldCombine = tk.BooleanVar(value=True)
        self.gaussian_algo = tk.StringVar(value="CV2")

        if oldOptions != None:
            self.threshold.set(oldOptions.threshold.get())
            self.framerate.set(oldOptions.framerate.get())
            self.compression_ratio.set(oldOptions.compression_ratio.get())
            self.scale_ratio.set(oldOptions.scale_ratio.get())
            self.kernel_size.set(oldOptions.kernel_size.get())
            self.bg_buffer_size.set(oldOptions.bg_buffer_size.get())
            self.motion_buffer_size.set(oldOptions.motion_buffer_size.get())
            self.min_size_ratio.set(oldOptions.min_size_ratio.get())
            self.shouldCombine.set(oldOptions.shouldCombine.get())
            self.gaussian_algo.set(oldOptions.gaussian_algo.get())
        self.option = tkinter.Toplevel()
        self.option.geometry("+1000+600")
        self.option.title("Options")
        self.tab = ttk.Notebook(self.option)  # Cr??ation du syst??me d'onglets
        self.t1 = ttk.Frame(self.tab)
        self.t2 = ttk.Frame(self.tab)
        self.t3 = ttk.Frame(self.tab)
        self.t4 = ttk.Frame(self.tab)
        self.t5 = ttk.Frame(self.tab)
        self.t6 = ttk.Frame(self.tab)
        self.tab.add(self.t1, text="General")
        self.tab.add(self.t2, text="Resize")
        self.tab.add(self.t3, text="Gaussian blur")
        self.tab.add(self.t4, text="Image buffer")
        self.tab.add(self.t5, text="Detection")
        self.tab.pack(expand=1, fill="both")

        self.add_tab1()
        self.add_tab2()
        self.add_tab3()
        self.add_tab4()
        self.add_tab5()

    # Recharge le module de traitement d'image avec les options
    def confirm_options(self):
        self.confirm()

    # Ajoute l'onglet d'option g??n??ral
    def add_tab1(self):
        self.l0 = Label(self.t1, text="Threshold", anchor="w")
        self.l0.grid(row=0, column=0, padx=10, pady=(15, 10))

        self.ent0 = Entry(self.t1, textvariable=self.threshold, width=21)
        self.ent0.place(width=150, height=50)
        self.ent0.grid(row=0, column=1, pady=5, padx=10)

        self.l1 = Label(self.t1, text="Framerate", anchor="w")
        self.l1.grid(row=1, column=0, padx=10, pady=10)

        self.ent1 = Entry(self.t1, textvariable=self.framerate, width=21)
        self.ent1.place(width=150, height=50)
        self.ent1.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t1, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    # Ajoute l'onglet d'option de compression d'image
    def add_tab2(self):
        self.l1 = Label(self.t2, text="Scale ratio", anchor="w")
        self.l1.grid(row=1, column=0, padx=10, pady=(15, 10))

        self.ent2 = Entry(self.t2, textvariable=self.scale_ratio, width=21)
        self.ent2.place(width=150, height=50)
        self.ent2.grid(row=1, column=1, pady=5, padx=10)

        self.l2 = Label(self.t2, text="Compression", anchor="w")
        self.l2.grid(row=2, column=0, padx=10, pady=10)

        self.ent3 = Entry(self.t2, textvariable=self.compression_ratio, width=21)
        self.ent3.place(width=150, height=50)
        self.ent3.grid(row=2, column=1, pady=5, padx=10)

        button = Button(self.t2, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=3, columnspan=2, padx=5, pady=5)

    # Ajoute l'onglet d'option du flou gaussien
    def add_tab3(self):
        vlist = ["CV2", "Custom"]

        self.l1 = Label(self.t3, text="Algorithme", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15, 10))

        self.combo = ttk.Combobox(
            self.t3, textvariable=self.gaussian_algo, values=vlist
        )
        self.combo.set("CV2")
        self.combo.grid(row=0, column=1, padx=5, pady=5)

        self.l2 = Label(self.t3, text="Kernel size", anchor="w")
        self.l2.grid(row=1, column=0, padx=10, pady=(15, 10))

        self.ent4 = Entry(self.t3, textvariable=self.kernel_size, width=21)
        self.ent4.place(width=150, height=50)
        self.ent4.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t3, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    # Ajoute l'onglet d'option des buffers
    def add_tab4(self):
        self.l1 = Label(self.t4, text="Motion Buffer size", anchor="w")
        self.l1.grid(row=0, column=0, padx=10, pady=(15, 10))

        self.ent6 = Entry(self.t4, textvariable=self.motion_buffer_size, width=21)
        self.ent6.place(width=150, height=50)
        self.ent6.grid(row=0, column=1, pady=5, padx=10)

        self.l2 = Label(self.t4, text="Background Buffer size", anchor="w")
        self.l2.grid(row=1, column=0, padx=10, pady=(15, 10))

        self.ent5 = Entry(self.t4, textvariable=self.bg_buffer_size, width=21)
        self.ent5.place(width=150, height=50)
        self.ent5.grid(row=1, column=1, pady=5, padx=10)

        button = Button(self.t4, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=2, columnspan=2, padx=5, pady=5)

    # Ajoute l'onglet d'option de la d??tection de mouvement
    def add_tab5(self):
        self.l1 = Label(self.t5, text="Min size ratio", anchor="w")
        self.l1.grid(row=1, column=0, padx=10, pady=(15, 10))

        self.ent7 = Entry(self.t5, textvariable=self.min_size_ratio, width=21)
        self.ent7.place(width=150, height=50)
        self.ent7.grid(row=1, column=1, pady=5, padx=10)

        self.l2 = Label(self.t5, text="Combine", anchor="w")
        self.l2.grid(row=2, column=0, padx=10, pady=(15, 10))

        self.ent8 = Checkbutton(
            self.t5, variable=self.shouldCombine, onvalue=True, offvalue=False, width=21
        )
        self.ent8.place(width=150, height=50)
        self.ent8.grid(row=2, column=1, pady=5, padx=10)

        button = Button(self.t5, text="Confirm", padx=24, command=self.confirm_options)
        button.grid(row=3, columnspan=2, padx=5, pady=5)


# Interface principale
class Interface(tk.Tk):
    # Initialisation de la fen??tre
    def __init__(self):
        tk.Tk.__init__(self)
        self.create_main()
        self.label = None
        self.motion_label = None
        self.stat = None
        self.thread = None
        self.alert_sent = False
        self.stat_isOpen = False
        self.last_frame_time = time()
        self.options = None
        self.label_all_stat1 = []
        self.label_all_stat2 = []
        self.label_all_stat3 = []
        self.mail = ""
        self.sms = ""
        # self.vs = VideoStream(src=0).start()
        # self.start_thread()

    # Cr??ation de boutons
    def create_main(self):
        button1 = Button(
            self,
            text="Source",
            width=10,
            command=partial(self.select_file),
        )
        button1.grid(row=1, column=0, padx=5, pady=5)

        button2 = Button(
            self,
            text="Motion filter",
            width=10,
            command=partial(self.open_motiom_filter),
        )
        button2.grid(row=1, column=1, padx=5, pady=5)

        button3 = Button(
            self,
            text="Stats",
            width=10,
            command=partial(self.open_stat),
        )
        button3.grid(row=1, column=2, padx=5, pady=5)

        button4 = Button(
            self,
            text="Options",
            width=10,
            command=partial(self.open_options),
        )
        button4.grid(row=1, column=3, padx=5, pady=5)

        button5 = Button(
            self,
            text="Set Alert",
            width=10,
            command=partial(self.select_alert),
        )
        button5.grid(row=1, column=4, padx=5, pady=5)

    def select_alert(self):
        self.select_alert_win = tk.Toplevel()
        self.select_alert_win.title("Select File")

        mail = tk.StringVar()
        sms = tk.StringVar()

        self.label_select_alert1 = Label(self.select_alert_win, text="Mail", anchor="w")
        self.label_select_alert1.grid(row=0, column=0, padx=10, pady=(15, 10))

        self.ent_select_alert1 = Entry(
            self.select_alert_win, textvariable=mail, width=21
        )
        self.ent_select_alert1.grid(row=0, column=1, pady=5, padx=10)

        self.label_select_alert2 = Label(self.select_alert_win, text="SMS", anchor="w")
        self.label_select_alert2.grid(row=1, column=0, padx=10, pady=(15, 10))

        self.ent_select_alert2 = Entry(
            self.select_alert_win, textvariable=sms, width=21
        )
        self.ent_select_alert2.grid(row=1, column=1, pady=5, padx=10)

        def confirm_select_alert():
            self.mail = mail.get()
            self.sms = sms.get()
            self.alert_sent = False
            self.select_alert_win.destroy()

        btn_confirm = Button(
            self.select_alert_win,
            text="Confirm",
            padx=24,
            command=confirm_select_alert,
        )
        btn_confirm.grid(row=2, columnspan=2, padx=5, pady=5)

    # Fonction de s??lection de fichier
    def select_file(self):
        self.select_file_win = tk.Toplevel()
        self.select_file_win.title("Select File")

        self.path = tk.StringVar()

        self.label_select_file = tk.Label(
            self.select_file_win, text="Select a file or put a link"
        )
        self.label_select_file.grid(row=0, columnspan=2, padx=10, pady=10)

        self.ent_select_file = Entry(
            self.select_file_win, textvariable=self.path, width=21
        )
        self.ent_select_file.place(width=150, height=50)
        self.ent_select_file.grid(row=1, column=0, pady=5, padx=10)

        button_browse = Button(
            self.select_file_win,
            text="Browse",
            width=10,
            command=partial(self.select_localfile),
        )
        button_browse.grid(row=1, column=1, padx=5, pady=5)

        button_confirm_file = Button(
            self.select_file_win,
            text="Confirm",
            width=10,
            command=partial(self.confirm_select_file),
        )
        button_confirm_file.grid(row=2, columnspan=2, padx=5, pady=5)

    def select_localfile(self):
        if self.thread != None:
            self.stop_thread()
        Tk().withdraw()
        fileName = askopenfilename()
        self.path.set(fileName)

    def confirm_select_file(self):
        self.vs = FileVideoStream(self.path.get()).start()
        self.start_thread()
        self.select_file_win.destroy()

    # Ouvre la vue du filtre d'image
    def open_motiom_filter(self):
        motion_filter = tk.Toplevel()
        motion_filter.geometry("+1000+100")
        motion_filter.title("Motion Filter")

        self.motion_label = tk.Label(motion_filter)
        self.motion_label.grid(row=0, columnspan=5, padx=10, pady=10)

    # Actualise les statistiques
    def add_stat(self):

        self.list_stat = performance_statistics.stats

        for i in range(len(self.list_stat)):
            self.label_all_stat1[i]["text"] = self.list_stat[i][0]
            self.label_all_stat2[i]["text"] = self.list_stat[i][1]

    # Ouvre la fen??tre de statistiques
    def open_stat(self):
        self.stat = tk.Toplevel()
        self.stat.geometry("+1000+350")
        self.stat.title("Statistiques")
        self.stat_isOpen = True

        self.list_stat = performance_statistics.stats
        self.label_stat_name = tk.Label(self.stat, text="Name")
        self.label_stat_name.grid(row=0, column=0, padx=10, pady=10)

        self.label_stat_average = tk.Label(self.stat, text="Average Time")
        self.label_stat_average.grid(row=0, column=1, padx=10, pady=10)

        self.label_all_stat1.clear()
        self.label_all_stat2.clear()

        for i in range(len(self.list_stat)):
            self.label_stat1 = tk.Label(self.stat, text=self.list_stat[i][0])
            self.label_stat1.grid(row=i + 1, column=0, padx=10, pady=10)

            self.label_stat2 = tk.Label(self.stat, text=self.list_stat[i][1])
            self.label_stat2.grid(row=i + 1, column=1, padx=10, pady=10)

            self.label_all_stat1.append(self.label_stat1)
            self.label_all_stat2.append(self.label_stat2)

    # Ouvre le menu d'options
    def open_options(self):
        self.options = Options(self, self.options, self.restart_thread)

    # Logique de traitement d'image et d'affichage pour chaque frame
    def video_loop(self):
        try:
            last_stat_update = 0
            while not self.thread.stopped():
                if self.options != None and self.options.framerate.get() > 0:
                    while (
                        time()
                        <= self.last_frame_time + 1 / self.options.framerate.get()
                    ):
                        pass
                self.last_frame_time = time()
                path = self.path.get()
                if path[0:4] == "http":
                    self.frame = get_image(self.path.get())
                else:
                    self.frame = self.vs.read()

                if self.frame is None:
                    break
                image = Image.fromarray(self.frame)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image, motion, detection, boxes = self.image_processing.process_image(
                    image
                )
                image = Image.fromarray(image.astype("uint8"))
                motion = Image.fromarray(motion.astype("uint8"))
                detection = Image.fromarray(detection.astype("uint8"))

                for box in boxes:
                    box.resize(detection.size[0], image.size[0])
                    image = self.draw_rectangle(image, box)
                proportion = 1
                if image.size[0] > image.size[1]:
                    proportion = 1280 / image.size[0]
                else:
                    proportion = 720 / image.size[1]
                newSize = (
                    int(image.size[0] * proportion),
                    int(image.size[1] * proportion),
                )
                image = Image.fromarray(
                    cv2.resize(
                        np.asarray(image),
                        newSize,
                        cv2.INTER_CUBIC,
                    ).astype("uint8")
                )
                self.display_image(image, self.label)
                if self.motion_label != None:
                    try:
                        self.display_image(motion, self.motion_label)
                    except:
                        self.motion_label = None
                if self.stat != None and time() - last_stat_update > 1:
                    try:
                        self.add_stat()
                    except:
                        self.stat = None
                    last_stat_update = time()
                if len(boxes) >= 1 and self.alert_sent == False:
                    if self.mail != "":
                        image.save("IPcam.png")
                        thread_send_email = threading.Thread(
                            target=lambda: send_alert.send_email(str(self.mail))
                        )
                        thread_send_email.start()
                        self.alert_sent = True
                    if self.sms != "":
                        thread_send_sms = threading.Thread(
                            target=lambda: send_alert.send_sms(str(self.sms))
                        )
                        thread_send_sms.start()
                        self.alert_sent = True
        except:
            return

    # Affiche l'image dans un label
    def display_image(self, image, label):
        self.image = ImageTk.PhotoImage(image)

        if label is None:
            label = tk.Label(image=self.image)
            label.grid(row=0, columnspan=5, padx=10, pady=10)
        else:
            label.configure(image=self.image)
        label.image = self.image

    # Dessine un rectangle ?? une position donn??e
    def draw_rectangle(self, image, box):
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (box.p1.y, box.p1.x, box.p2.y, box.p2.x), fill=None, outline="red"
        )
        return image

    # Restart le thread de filtrage/d??tection de mouvement
    def restart_thread(self):
        if self.thread != None:
            self.stop_thread()
        self.start_thread()

    # Tue le thread
    def stop_thread(self):
        self.thread.stop()
        self.thread.join(timeout=0.05)

    # Commence le thread avec les settings appropri??s pour le traitement d'image
    def start_thread(self):
        if self.options != None:
            self.image_processing = ImageProcessing(
                self.options.threshold.get(),
                self.options.scale_ratio.get(),
                self.options.compression_ratio.get(),
                self.options.bg_buffer_size.get(),
                self.options.motion_buffer_size.get(),
                self.options.kernel_size.get(),
                self.options.gaussian_algo.get(),
                self.options.min_size_ratio.get(),
                self.options.shouldCombine.get(),
            )
        else:
            self.image_processing = ImageProcessing()
        self.thread = StoppableThread(target=self.video_loop, args=())
        self.thread.daemon = True
        self.thread.start()

    # Fonction pour fermer l'application
    def quit(self):
        self.master.destroy()


# Init l'application
if __name__ == "__main__":
    root = Interface()
    root.title("Motion detection")
    root.mainloop()
    if root.thread != None:
        root.thread.stop()
        root.thread.join(timeout=0.05)
