from gui.gui_main import gui_main

class Main:    
    def run(self):
        self.run_main_gui()   
        
    def run_main_gui(self):
        g_main_title = "EvE Industry Tycoon"
        g_main_width = 800
        g_main_height = 600
        
        main_window = gui_main(title=g_main_title, height=g_main_height, width=g_main_width)
        main_window.run_window()

if __name__ == '__main__':
    Main().run()

