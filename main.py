from log import log
from gui.gui_main import gui_main

class Main:    
    
    # main execution flow
    def run(self):
        main_window = gui_main(None, None, None)
        main_window.run_window()
       

if __name__ == '__main__':
    Main().run()

