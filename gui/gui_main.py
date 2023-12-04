import tkinter as tk
from logic import logic

class gui_main:
    
    def __init__(self, title, height, width):
        self.title = "EvE Industry Tycoon"
        self.height = 600
        self.width = 800


    def run_window(self):        
        window = tk.Tk()
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
        sync_menu.add_command(label="Update SDE", command=lambda: logic.sde_update(self))
        menubar.add_cascade(label="Sync", menu=sync_menu)
        
        # add exit
        menubar.add_command(label="Exit", command=window.quit)
        
        window.config(menu=menubar)
        return menubar

        

        

  