import tkinter as tk
from PIL import Image, ImageTk

from lib.logger import logger
from lib.gui.gui_main import gui_main

class navbar(gui_main):
    """A navigation bar element, used in main UI window
    """
    def __init__(self, log: logger, window: tk):
        self.log = log
        self.window = window
        self.frame = tk.Frame()


    # run this to initialize whole navbar
    def navbar_init(self):
        self.frame_configure()
        self.frame_add_buttons()
        self.frame_pack()
        self.on_startup()
        return self.frame


    def frame_configure(self):
        self.frame.master = self.window
        self.frame.config(width=34)
        self.frame.config(highlightbackground="gray")
        self.frame.config(highlightthickness=1)


    def frame_pack(self):
        self.frame.pack_configure(fill=tk.BOTH)
        self.frame.pack_configure(side=tk.LEFT)
        self.frame.pack_configure(expand=False)
        self.frame.pack


    # whenever a button is pressed - forward selected mode to parent class
    def on_button_pressed(self, mode: str):
        self.frame_main_switch_mode(mode)


    # initial mode on app start
    def on_startup(self):
        mode = 'market'
        self.frame_main_switch_mode(mode)


    def frame_add_buttons(self):
        self.add_button_market(side='top')
        self.add_button_contracts(side='top')
        self.add_button_industry(side='top')
        self.add_button_assets(side='top')
        self.add_button_map(side='top')
        self.add_button_debug(side='bottom')


    def add_button_market(self, side: str):
        path = 'assets/gui/nav_panel/Market.png'
        global img_nav_market
        img_nav_market = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Market')
        btn.config(image=img_nav_market)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('market'))
        btn.pack(fill='x', side=side)


    def add_button_contracts(self, side: str):
        path = 'assets/gui/nav_panel/Contracts.png'
        global img_nav_contracts
        img_nav_contracts = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Contracts')
        btn.config(image=img_nav_contracts)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('contracts'))
        btn.pack(fill='x', side=side)


    def add_button_industry(self, side: str):
        path = 'assets/gui/nav_panel/Industry.png'
        global img_nav_industry
        img_nav_industry = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Industry')
        btn.config(image=img_nav_industry)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('industry'))
        btn.pack(fill='x', side=side)


    def add_button_assets(self, side: str):
        path = 'assets/gui/nav_panel/Assets.png'
        global img_nav_assets
        img_nav_assets = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Assets')
        btn.config(image=img_nav_assets)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('assets'))
        btn.pack(fill='x', side=side)


    def add_button_map(self, side: str):
        path = 'assets/gui/nav_panel/Map.png'
        global img_nav_map
        img_nav_map = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Map')
        btn.config(image=img_nav_map)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('map'))
        btn.pack(fill='x', side=side)


    def add_button_debug(self, side: str):
        path = 'assets/gui/nav_panel/Debug.png'
        global img_nav_debug
        img_nav_debug = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.frame, width=46, height=64)
        btn.config(text='Debug')
        btn.config(image=img_nav_debug)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.on_button_pressed('debug'))
        btn.pack(fill='x', side=side)