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
        self.status = tk.Frame()
        
        self.main = tk.Frame()
        self.main_market = tk.Frame()
        self.main_contracts = tk.Frame()
        self.main_industry = tk.Frame()
        self.main_assets = tk.Frame()
        self.main_map = tk.Frame()
        self.main_debug = tk.Frame()
        
        self.main_frames = {
            'main'      : self.main,
            'market'    : self.main_market,
            'contracts' : self.main_contracts,
            'industry'  : self.main_industry,
            'assets'    : self.main_assets,
            'map'       : self.main_map,
            'debug'     : self.main_debug
        }


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
        self.frame_main_market_init()
        self.frame_main_contracts_init()
        self.frame_main_industry_init()
        self.frame_main_assets_init()
        self.frame_main_map_init()
        self.frame_main_debug_init()
        
        self.frame_main_switch_mode('main')


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
        swagger_menu = tk.Menu(menu, tearoff=0)
        swagger_menu.add_command(label="Sync All", 
                                command='')
        swagger_menu.add_separator()
        swagger_menu.add_command(label="Sync Universe regions", 
                                command=lambda: self.menubar_esi_sync_regions())
        menu.add_cascade(label="Swagger data (ESI)", menu=swagger_menu)
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


    def menubar_esi_sync_regions(self):
        self.logic.esi_sync_regions()
        messagebox.showinfo("Regions updates", "All regions fetched and updated from ESI.")


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


    # main area basic style template
    def frame_main_init_template(self, frame:tk.Frame):
        frame.config(height=600)
        frame.config(width=800)
        frame.config(highlightbackground="gray")
        frame.config(highlightthickness=1)
        frame.pack_forget()
        return frame
        

    # main area when no nav section is selected
    def frame_main_init(self):
        frame = self.frame_main_init_template(self.main)
        
        nav_label = tk.Label(master=frame, text="Main panel.\nSelect Section in navbar to continue.")
        nav_label.pack(side="top")


    # market area
    def frame_main_market_init(self):
        frame = self.frame_main_init_template(self.main_market)
        
        market_label = tk.Label(master=frame, text="Market\nWIP")
        market_label.pack(side="top")


    # contracts area
    def frame_main_contracts_init(self):
        frame = self.frame_main_init_template(self.main_contracts)
        
        market_label = tk.Label(master=frame, text="Contracts\nWIP")
        market_label.pack(side="top")


    # industry area
    def frame_main_industry_init(self):
        frame = self.frame_main_init_template(self.main_industry)
        
        market_label = tk.Label(master=frame, text="Industry\nWIP")
        market_label.pack(side="top")


    # assets area
    def frame_main_assets_init(self):
        frame = self.frame_main_init_template(self.main_assets)
        
        market_label = tk.Label(master=frame, text="Assets\nWIP")
        market_label.pack(side="top")


    # map area
    def frame_main_map_init(self):
        frame = self.frame_main_init_template(self.main_map)
        
        market_label = tk.Label(master=frame, text="Map\nWIP")
        market_label.pack(side="top")


    # debug section for messing aroung
    def frame_main_debug_init(self):
        frame = self.frame_main_init_template(self.main_debug)
        
        market_label = tk.Label(master=frame, text="Debug")
        market_label.pack(side="top")
        
        # to be deleted
        esi_tst_btn = tk.Button(frame)
        esi_tst_btn.config(text='ESI TEST')
        esi_tst_btn.config(command=lambda: self.logic.esi_test())
        esi_tst_btn.pack(side='top')
        self.main_debug.pack_forget()


    # hide active main frame and display selected
    def frame_main_switch_mode(self, mode:str):
        for frame in self.main_frames:
            if frame!=mode:
                self.main_frames[frame].pack_forget()
            else:
                self.main_frames[frame].pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


    def btn_click_esi_test(self, txtbox: tk.Text):
        result = self.logic.esi_test()
        txtbox.delete(1.0, tk.END)
        txtbox.insert(tk.END, result)