import tkinter as tk
from tkinter import messagebox
from lib.logger import logger
from logic import logic
# from lib.gui.gui_main import gui_main

class menubar:

    def __init__(self, log: logger, logic: logic, window: tk):
        self.log = log
        self.logic = logic
        self.window = window


    # create menubar instance
    def create_menubar(self):
        menu = tk.Menu(self.window)
        # add main menu
        self.menu = self.menubar_add_main(menu)
        # add character menu
        self.menu = self.menubar_add_char(menu)
        # add sync menu
        self.menu = self.menubar_add_sync(menu)
        # add exit
        self.menu.add_command(label="Exit", command=lambda: self.menu_exit())

        self.window.config(menu=menu)
        return self.menu


    # add main menu
    def menubar_add_main(self, menubar:tk.Menu):
        menu = tk.Menu(menubar, tearoff=0)
        #main_menu.add_command(label="Settings", command=0)
        menubar.add_cascade(label="Main", menu=menu)
        return menubar


    # add character menu
    def menubar_add_char(self,menubar:tk.Menu):
        menu = tk.Menu(menubar, tearoff=0)
        menu.add_command(label="Add character (SSO)", command='')
        
        char = tk.Menu(menubar, tearoff=0)
        char.add_command(label="Refresh", command='')
        char.add_command(label="Delete", command='')
        menu.add_cascade(label="Character Dummy", menu=char)
        
        menubar.add_cascade(label="Characters", menu=menu)
        return menubar


    # add data sync menu
    def menubar_add_sync(self,menubar:tk.Menu):
        menu = tk.Menu(menubar, tearoff=0)
        
        # add SDE submenu
        sde_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Static data (SDE)", menu=sde_menu)
        sde_menu.add_command(label="Download yaml", command=lambda: self.menu_update_sde())
        sde_menu.add_command(label="Parse yaml 2 sql", command=lambda: self.menu_sde_2_db())
        
        menu.add_command(label="Image Collection (IEC)", command=lambda: self.menu_import_images())
        menubar.add_cascade(label="Sync", menu=menu)
        return menubar


    # add exit button
    def menu_exit(self):
        result = messagebox.askyesno("Exiting", "Closing, eh?")
        if result:
            self.window.destroy()
        else:
            return


    # download graphics
    def menu_import_images(self):
        self.logic.icons_download()
        messagebox.showinfo("Icons downloaded", "Icons downloaded and extracted.")


    # Check and download fresh SDE files
    def menu_update_sde(self):
        self.logic.sde_update()
        messagebox.showinfo("Update Complete", "SDE Update Finished!")


    # parse local SDE yaml 2 sqlite
    def menu_sde_2_db(self):
        # start the progressbar
        # self.progressbar.start()
        # refresh the GUI and fire it's callbacks
        # self.window.update()
        # self.window.update_idletasks()
        # start the updater
        # TODO: We should feed the progressbar with some variable to indicate
        # the actual progress. The logic/updater class should be able to export
        # this value so the GUI can be updated with it.
        self.logic.sde_2_db()
        # stop the progressbar
        # self.progressbar.stop()
        messagebox.showinfo("Parsing Complete", "YAML files imported")