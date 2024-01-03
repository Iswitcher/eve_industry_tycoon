from lib.logger         import logger
from lib.gui.gui_main   import gui_main
from logic              import logic

class Main:
    # main execution flow
    def run(self, log: logger):
        main_logic = logic(log)
        main_window = gui_main(log, main_logic)
        main_window.run_window()


if __name__ == '__main__':
    log = logger(log_to_file=True)
    Main().run(log)
