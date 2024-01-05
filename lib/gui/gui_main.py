# import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from logic import logic
from lib.logger import logger

from lib.gui.main.menubar import menubar
# from lib.gui.main.navbar import navbar

class gui_main:

    def __init__(self, log:logger, logic:logic):
        self.log = log
        self.logic = logic
        
        self.title = "EvE Industry Tycoon"
        self.width = 1024
        self.height = 768
        
        self.window = tk.Tk()
        
        self.menu = menubar(self.log, self.logic, self.window)
        self.utils = tk.Frame()
        
        from lib.gui.main.navbar import navbar
        self.navbar = navbar(self.log, self.window)
        
        self.main = tk.Frame()
        self.status = tk.Frame()


    def run_window(self):
        self.window.title(self.title)
        self.window.minsize(self.width, self.height)
        self.window.geometry(f"{self.width}x{self.height}")
        
        self.set_window_layout()
        
        self.window.mainloop()


    def set_window_layout(self):
        # add dropdown menubar
        self.menu.create_menubar()
        
        # add bottom area for status text and progressbars
        self.init_frame_status()
        self.populate_frame_status()

        # universal tools?
        self.init_frame_utils()
        self.populate_frame_utils()
        
        # navigation frame
        self.navbar.navbar_init()
        
        # main area, content depends on selected nav menu
        self.init_frame_main()
        self.populate_frame_main()


    def init_frame_status(self):
        self.status.master = self.window
        self.status.config(height=10)
        self.status.config(highlightbackground="gray")
        self.status.config(highlightthickness=1)
        
        self.status.pack_configure(fill=tk.BOTH)
        self.status.pack_configure(side=tk.BOTTOM)
        self.status.pack_configure(expand=False)
        self.status.pack


    def init_frame_utils(self):
        self.utils.master = self.window
        self.utils.config(height=50)
        self.utils.config(bg="light gray")
        self.utils.config(highlightbackground="gray")
        self.utils.config(highlightthickness=1)
        
        self.utils.pack_configure(fill=tk.BOTH)
        self.utils.pack_configure(side=tk.TOP)
        self.utils.pack_configure(expand=False)
        self.utils.pack


    def init_frame_main(self):
        self.main.master = self.window
        self.main.config(height=600)
        self.main.config(width=800)
        self.main.config(highlightbackground="gray")
        self.main.config(highlightthickness=1)
        
        self.main.pack_configure(fill=tk.BOTH)
        self.main.pack_configure(side=tk.LEFT)
        self.main.pack_configure(expand=True)


    def populate_frame_status(self):
        # add progressbar
        self.progressbar = ttk.Progressbar(orient="horizontal", master=self.status)
        self.progressbar.pack(fill='x', side="right", padx=6, pady=3)
        
        utils_label = tk.Label(master=self.status, text="Status panel")
        utils_label.place(x=0, y=0) 


    def populate_frame_utils(self):
        utils_label = tk.Label(master=self.utils, text="App tools panel")
        utils_label.place(x=0, y=0) 


    def populate_frame_main(self):        
        nav_label = tk.Label(master=self.main, text="Main panel")
        nav_label.pack(side="top")


    def btn_click_esi_test(self, txtbox: tk.Text):
        result = self.logic.esi_test()
        txtbox.delete(1.0, tk.END)
        txtbox.insert(tk.END, result)


    def frame_main_switch_mode(self, mode:str):
        # TODO switch main frame based on imput
        blah = 123