import time
import fcntl
import os
import signal
import os

import neovim

FOLDER_NAME = "/tmp/colors/"
COLOR_FILE_NAME = "vimtheme"

THEME_PATH = FOLDER_NAME + COLOR_FILE_NAME

@neovim.plugin
class ColorChanger(object):
    def __init__(self, vim):
        self.vim = vim
        

    @neovim.command('ReadNewColorscheme', range='', nargs='*', sync=True)
    def readColorScheme(self, args, range):
        f = open(THEME_PATH, 'r')

        colorscheme = f.readline().replace("\n", "")
        self.vim.command("colorscheme {}".format(colorscheme))

        f.close()


    def folderChangeHandler(self, signum, frame):
        self.vim.command("ReadNewColorscheme")
        

    def ensureFilesExist(self):
        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)

        #If there is no file containing a color theme already
        if not os.path.isfile(THEME_PATH):
            #Create the file with the current theme in it
            f = open(THEME_PATH, 'w')

            f.write(self.vim.command_output("colorscheme").replace("\n", ""))

            f.close()
            




    @neovim.command('StartColorPoll', range='', nargs='*', sync=False)
    def command_handler(self, args, range):
        self.ensureFilesExist();

        signal.signal(signal.SIGIO, self.folderChangeHandler)
        fd = os.open(FOLDER_NAME,  os.O_RDONLY)
        fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
        fcntl.fcntl(fd, fcntl.F_NOTIFY,
                    fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

        #Sleep indefinetly while waiting for change events
        while True:
            time.sleep(10000)

