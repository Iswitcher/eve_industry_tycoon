from lib.gui.gui_main import gui_main
from lib.logger import logger

class Main:
    # main execution flow
    def run(self, log: logger):
        main_window = gui_main(log, "EvE Industry Tycoon", 800, 600)
        main_window.run_window()


if __name__ == '__main__':
    log = logger(log_to_file=True)
    Main().run(log)
