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
        sync_menu.add_command(label="Import Images", command=lambda: self.menu_import_images())
        sync_menu.add_command(label="Update SDE", command=lambda: self.menu_update_sde())
        sync_menu.add_command(label="SDE 2 DB", command=lambda: self.menu_sde_2_db())
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