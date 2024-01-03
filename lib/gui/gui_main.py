# import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from logic import logic
from lib.logger import logger
from lib.gui.main.menubar import menubar

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
        nav_frame = self.init_frame_navigation(window)
        self.populate_frame_navigation(nav_frame)
        
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
        frame.config(bg="gray")
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        
        frame.pack_configure(fill=tk.BOTH)
        frame.pack_configure(side=tk.TOP)
        frame.pack_configure(expand=False)
        frame.pack
        return frame


    def init_frame_navigation(self, parent):
        frame = tk.Frame(master=parent)
        frame.config(width=34)
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        
        frame.pack_configure(fill=tk.BOTH)
        frame.pack_configure(side=tk.LEFT)
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


    def populate_frame_navigation(self, frame):
        path_nav_market = 'assets/gui/nav_panel/Market.png'
        global img_nav_market
        img_nav_market = ImageTk.PhotoImage(Image.open(path_nav_market).resize((32,32)))
        market_btn = tk.Button(frame, text='Market', image=img_nav_market,compound="top", width=32, height=32)
        market_btn.pack(fill='x', side='top')
        
        path_contracts = 'assets/gui/nav_panel/Market.png'
        global img_contracts
        img_contracts = ImageTk.PhotoImage(Image.open(path_contracts).resize((32,32)))
        contracts_btn = tk.Button(frame, text='Contracts', image=img_contracts, width=32, height=32)
        contracts_btn.pack(fill='x', side='top')
        
        path_industry = 'assets/gui/nav_panel/Market.png'
        global img_industry
        img_industry = ImageTk.PhotoImage(Image.open(path_industry).resize((32,32)))
        industry_btn = tk.Button(frame, text='Industry', image=img_industry, width=32, height=32)
        industry_btn.pack(fill='x', side='top')
        
        path_assets = 'assets/gui/nav_panel/Market.png'
        global img_assets
        img_assets = ImageTk.PhotoImage(Image.open(path_assets).resize((32,32)))
        assets_btn = tk.Button(frame, text='Assets', image=img_assets, width=32, height=32)
        assets_btn.pack(fill='x', side='top')
        
        path_map = 'assets/gui/nav_panel/Market.png'
        global img_map
        img_map = ImageTk.PhotoImage(Image.open(path_map).resize((32,32)))
        map_btn = tk.Button(frame, text='Map', image=img_map, width=32, height=32)
        map_btn.pack(fill='x', side='top')
        
        path_debug = 'assets/gui/nav_panel/Market.png'
        global img_debug
        img_debug = ImageTk.PhotoImage(Image.open(path_debug).resize((32,32)))
        debug = tk.Button(frame, text='Debug', image=img_debug, width=32, height=32)
        debug.pack(fill='x', side='bottom')


    def populate_frame_main(self, frame):        
        nav_label = tk.Label(master=frame, text="Main panel")
        nav_label.pack(side="top")

    def btn_click_esi_test(self, txtbox: tk.Text):
        result = self.logic.esi_test()
        txtbox.delete(1.0, tk.END)
        txtbox.insert(tk.END, result)