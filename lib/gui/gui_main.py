# import threading
import tkinter as tk
from tkinter import messagebox

from logic import logic


class gui_main:
    
    def __init__(self, title, height, width):
        self.title = "EvE Industry Tycoon"
        self.height = 600
        self.width = 800
        self.window = tk.Tk()
        self.logic = logic()


    def run_window(self):
             
        self.window.title(self.title)
        self.window.geometry(f"{self.width}x{self.height}")
        self.create_menubar(self.window)
        
        self.window.mainloop()
                

    def create_menubar(self, window):
        menubar = tk.Menu(window)
        
        # add main menu
        main_menu = tk.Menu(menubar, tearoff=0)
        #main_menu.add_command(label="Settings", command=0)
        menubar.add_cascade(label="Main", menu=main_menu)
        
        # add sync menu
        sync_menu = tk.Menu(menubar, tearoff=0)
        # add SDE submenu
        sde_menu = tk.Menu(sync_menu, tearoff=0)
        sde_menu.add_command(label="SDE Download", command=lambda: self.menu_update_sde())
        sde_menu.add_command(label="Parse SDE to db", command=lambda: self.menu_sde_2_db())
        
        sync_menu.add_cascade(label="Static data (SDE)", menu=sde_menu)
        sync_menu.add_command(label="Import Images (WIP)", command=lambda: self.menu_import_images())
        menubar.add_cascade(label="Sync", menu=sync_menu)
        
        # add exit
        menubar.add_command(label="Exit", command=lambda: self.menu_exit())
        
        window.config(menu=menubar)
        return menubar
    
    
    # exit?
    def menu_exit(self):
        result = messagebox.askyesno("Exiting", "Closing, eh?")
        if result:
            self.window.destroy()
        else:
            return


    # download graphics
    def menu_import_images(self):
        messagebox.showinfo("Move along!", "Not yet implemented")
    
    
    # Check and download fresh SDE files
    def menu_update_sde(self):
        self.logic.sde_update()
        messagebox.showinfo("Update Complete", "SDE Update Finished!")
        
    
    # parse local SDE yaml 2 sqlite
    def menu_sde_2_db(self):
        self.logic.sde_2_db()
        messagebox.showinfo("Parsing Complete", "YAML files imported")