# import threading
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk

from logic import logic
from lib.logger import logger

class gui_main:

    def __init__(self, log:logger, logic:logic):
        self.log = log
        self.logic = logic
        
        self.title = "EvE Industry Tycoon"
        self.width = 1024
        self.height = 768
        self.window = tk.Tk()
        self.menu = tk.Menu()
        
        self.utils = tk.Frame()
        self.navbar = tk.Frame()
        self.main = tk.Frame()
        self.status = tk.Frame()


    # init window and its components, launch it
    def run_window(self):
        self.window.title(self.title)
        self.window.minsize(self.width, self.height)
        self.window.geometry(f"{self.width}x{self.height}")
        
        self.set_window_layout()
        self.window.mainloop()


    # init window components, frames
    def set_window_layout(self):
        # add dropdown menubar
        self.menubar_init()
        # add bottom area for status text and progressbars
        self.frame_status_init()
        # universal tools bar
        self.frame_utils_init()
        # navigation panel
        self.frame_navbar_init()
        # main area, content depends on selected nav menu
        self.frame_main_init()


    # add window top menubar with dropdown options/actions
    def menubar_init(self):
        # add main menu
        self.menu = self.menubar_add_main(self.menu)
        # add character menu
        self.menu = self.menubar_add_char(self.menu)
        # add sync menu
        self.menu = self.menubar_add_sync(self.menu)
        # add exit
        self.menu.add_command(label="Exit", command=lambda: self.window_exit())
        self.window.config(menu=self.menu)


    # add main section of menubar
    def menubar_add_main(self, master: tk.Menu):
        menu = tk.Menu(master, tearoff=0)
        #main_menu.add_command(label="Settings", command=0)
        master.add_cascade(label="Main", menu=menu)
        return master


    # add character section of menubar
    def menubar_add_char(self, master: tk.Menu):
        menu = tk.Menu(master, tearoff=0)
        menu.add_command(label="Add character (SSO)", command='')
        
        char = tk.Menu(master, tearoff=0)
        char.add_command(label="Refresh", command='')
        char.add_command(label="Delete", command='')
        menu.add_cascade(label="Character Dummy", menu=char)
        
        master.add_cascade(label="Characters", menu=menu)
        return master


    # add data sync menu
    def menubar_add_sync(self,master: tk.Menu):
        menu = tk.Menu(master, tearoff=0)  
        # add SDE submenu
        sde_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Static data (SDE)", menu=sde_menu)
        sde_menu.add_command(label="Download yaml", 
                             command=lambda: self.menubar_update_sde())
        sde_menu.add_command(label="Parse yaml 2 sql", 
                             command=lambda: self.menubar_sde_2_db())
        menu.add_command(label="Image Collection (IEC)", 
                         command=lambda: self.menubar_import_images())
        master.add_cascade(label="Sync", menu=menu)
        return master


    # Check and download fresh SDE files
    def menubar_update_sde(self):
        self.logic.sde_update()
        messagebox.showinfo("Update Complete", "SDE Update Finished!")


    # download graphics
    def menubar_import_images(self):
        self.logic.icons_download()
        messagebox.showinfo("Icons downloaded", "Icons downloaded and extracted.")


    # parse local SDE yaml 2 sqlite
    def menubar_sde_2_db(self):
        # start the progressbar
        self.progressbar.start()
        # refresh the GUI and fire it's callbacks
        self.window.update()
        self.window.update_idletasks()
        # start the updater
        # TODO: We should feed the progressbar with some variable to indicate
        # the actual progress. The logic/updater class should be able to export
        # this value so the GUI can be updated with it.
        self.logic.sde_2_db()
        # stop the progressbar
        # self.progressbar.stop()
        messagebox.showinfo("Parsing Complete", "YAML files imported")


    # menubar exit button
    def window_exit(self):
        result = messagebox.askyesno("Exiting", "Closing, eh?")
        if result:
            self.window.destroy()
        else:
            return


    # add bottom statusbar
    def frame_status_init(self):
        self.status.master = self.window
        self.status.config(height=10)
        self.status.config(highlightbackground="gray")
        self.status.config(highlightthickness=1)
        
        # add progressbar
        self.progressbar = ttk.Progressbar(orient="horizontal", master=self.status)
        self.progressbar.pack(fill='x', side="right", padx=6, pady=3)
        # add dummy label
        utils_label = tk.Label(master=self.status, text="Status panel")
        utils_label.place(x=0, y=0) 
        
        self.status.pack_configure(fill=tk.BOTH)
        self.status.pack_configure(side=tk.BOTTOM)
        self.status.pack_configure(expand=False)
        self.status.pack


    # TODO: decide, is the utils bar a part of main or not, for now its a dummy
    def frame_utils_init(self):
        self.utils.master = self.window
        self.utils.config(height=50)
        self.utils.config(bg="light gray")
        self.utils.config(highlightbackground="gray")
        self.utils.config(highlightthickness=1)
        
        utils_label = tk.Label(master=self.utils, text="App tools panel")
        utils_label.place(x=0, y=0) 
        
        # to be deleted
        esi_tst_btn = tk.Button(self.utils)
        esi_tst_btn.config(text='ESI TEST')
        esi_tst_btn.config(command=lambda: self.logic.esi_test())
        esi_tst_btn.pack(fill='x', side='right')
        
        self.utils.pack_configure(fill=tk.BOTH)
        self.utils.pack_configure(side=tk.TOP)
        self.utils.pack_configure(expand=False)
        self.utils.pack


    # navigation bar, switches modes for main frame
    def frame_navbar_init(self):
        self.navbar.master = self.window
        self.navbar.config(width=34)
        self.navbar.config(highlightbackground="gray")
        self.navbar.config(highlightthickness=1)
        
        self.navbar_add_market(side='top')
        self.navbar_add_contracts(side='top')
        self.navbar_add_industry(side='top')
        self.navbar_add_assets(side='top')
        self.navbar_add_map(side='top')
        self.navbar_add_debug(side='bottom')
        
        self.navbar.pack_configure(fill=tk.BOTH)
        self.navbar.pack_configure(side=tk.LEFT)
        self.navbar.pack_configure(expand=False)
        self.navbar.pack


    def navbar_add_market(self, side: str):
        path = 'assets/gui/nav_panel/Market.png'
        global img_nav_market
        img_nav_market = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Market')
        btn.config(image=img_nav_market)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('market'))
        btn.pack(fill='x', side=side)


    def navbar_add_contracts(self, side: str):
        path = 'assets/gui/nav_panel/Contracts.png'
        global img_nav_contracts
        img_nav_contracts = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Contracts')
        btn.config(image=img_nav_contracts)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('contracts'))
        btn.pack(fill='x', side=side)


    def navbar_add_industry(self, side: str):
        path = 'assets/gui/nav_panel/Industry.png'
        global img_nav_industry
        img_nav_industry = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Industry')
        btn.config(image=img_nav_industry)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('industry'))
        btn.pack(fill='x', side=side)


    def navbar_add_assets(self, side: str):
        path = 'assets/gui/nav_panel/Assets.png'
        global img_nav_assets
        img_nav_assets = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Assets')
        btn.config(image=img_nav_assets)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('assets'))
        btn.pack(fill='x', side=side)


    def navbar_add_map(self, side: str):
        path = 'assets/gui/nav_panel/Map.png'
        global img_nav_map
        img_nav_map = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Map')
        btn.config(image=img_nav_map)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('map'))
        btn.pack(fill='x', side=side)


    def navbar_add_debug(self, side: str):
        path = 'assets/gui/nav_panel/Debug.png'
        global img_nav_debug
        img_nav_debug = ImageTk.PhotoImage(Image.open(path).resize((42,42)))
        btn = tk.Button(self.navbar, width=46, height=64)
        btn.config(text='Debug')
        btn.config(image=img_nav_debug)
        btn.config(compound='top')
        btn.config(width=46)
        btn.config(height=64)
        btn.config(command=lambda: self.frame_main_switch_mode('debug'))
        btn.pack(fill='x', side=side)


    def frame_main_init(self):
        self.main.master = self.window
        self.main.config(height=600)
        self.main.config(width=800)
        self.main.config(highlightbackground="gray")
        self.main.config(highlightthickness=1)
        
        nav_label = tk.Label(master=self.main, text="Main panel.\nSelect Section in navbar to continue.")
        nav_label.pack(side="top")
        
        self.main.pack_configure(fill=tk.BOTH)
        self.main.pack_configure(side=tk.LEFT)
        self.main.pack_configure(expand=True)


    def btn_click_esi_test(self, txtbox: tk.Text):
        result = self.logic.esi_test()
        txtbox.delete(1.0, tk.END)
        txtbox.insert(tk.END, result)


    def frame_main_switch_mode(self, mode:str):
        self.main.destroy()
        # TODO switch main frame based on imput
        blah = 123