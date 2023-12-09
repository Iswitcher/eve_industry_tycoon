import threading
from tkinter import messagebox

import tkinter as tk
window = tk.Tk()

from logic import logic
lg = logic() 


class gui_main:
    
    def __init__(self, title, height, width):
        self.title = "EvE Industry Tycoon"
        self.height = 600
        self.width = 800


    def run_window(self):
             
        window.title(self.title)
        window.geometry(f"{self.width}x{self.height}")
        self.create_menubar(window)
        
        window.mainloop()
                

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
            window.destroy()
        else:
            return


    # download graphics
    def menu_import_images(self):
        messagebox.showinfo("Move along!", "Not yet implemented")
    
    
    # Check and download fresh SDE files
    def menu_update_sde(self):
        lg.sde_update()
        messagebox.showinfo("Update Complete", "SDE Update Finished!")
        
    
    # parse local SDE yaml 2 sqlite
    def menu_sde_2_db(self):
        lg.sde_2_db()
        messagebox.showinfo("Parsing Complete", "YAML files imported")