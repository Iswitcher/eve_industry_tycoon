# import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from logic import logic
from lib.logger import logger

from lib.gui.main.menubar import menubar
from lib.gui.main.navbar import navbar

class gui_main:

    def __init__(self, log:logger, logic:logic):
        self.log = log
        self.logic = logic
        
        self.title = "EvE Industry Tycoon"
        self.width = 1024
        self.height = 768
        
        self.window = tk.Tk()


    def run_window(self):
        self.window.title(self.title)
        self.window.minsize(self.width, self.height)
        self.window.geometry(f"{self.width}x{self.height}")
        
        menu = menubar(self.log, self.logic, self.window)
        menu.create_menubar()
        
        self.set_layout(self.window)
        self.window.mainloop()


    def set_layout(self, window):
        # add bottom area for status text and progressbars
        status_frame = self.init_frame_status(window)
        self.populate_frame_status(status_frame)

        # universal tools?
        utils_frame = self.init_frame_utils(window)
        self.populate_frame_utils(utils_frame)
        
        # navigation frame
        nav_frame = navbar(self.log, self.logic, self.window)
        nav_frame.navbar_init()
        
        # main area, content depends on selected nav menu
        main = self.init_frame_main(window)
        self.populate_frame_main(main)


    def init_frame_status(self, parent):
        frame = tk.Frame(master=parent)
        frame.config(height=10)
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        
        frame.pack_configure(fill=tk.BOTH)
        frame.pack_configure(side=tk.BOTTOM)
        frame.pack_configure(expand=False)
        frame.pack
        return frame


    def init_frame_utils(self, parent):
        frame = tk.Frame(master=parent)
        frame.config(height=50)
        frame.config(bg="light gray")
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        
        frame.pack_configure(fill=tk.BOTH)
        frame.pack_configure(side=tk.TOP)
        frame.pack_configure(expand=False)
        frame.pack
        return frame


    def init_frame_main(self, parent):
        frame = tk.Frame(master=parent)
        frame.config(height=600)
        frame.config(width=800)
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        
        frame.pack_configure(fill=tk.BOTH)
        frame.pack_configure(side=tk.LEFT)
        frame.pack_configure(expand=True)
        return frame


    def populate_frame_status(self, frame):
        # add progressbar
        self.progressbar = ttk.Progressbar(orient="horizontal", master=frame)
        self.progressbar.pack(fill='x', side="right", padx=6, pady=3)
        
        utils_label = tk.Label(master=frame, text="Status panel")
        utils_label.place(x=0, y=0) 


    def populate_frame_utils(self, frame):
        utils_label = tk.Label(master=frame, text="App tools panel")
        utils_label.place(x=0, y=0) 


    def populate_frame_main(self, frame):        
        nav_label = tk.Label(master=frame, text="Main panel")
        nav_label.pack(side="top")


    def btn_click_esi_test(self, txtbox: tk.Text):
        result = self.logic.esi_test()
        txtbox.delete(1.0, tk.END)
        txtbox.insert(tk.END, result)