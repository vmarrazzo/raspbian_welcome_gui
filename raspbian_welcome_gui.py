__author__ = "Vincenzo Marrazzo"
__copyright__ = "Copyright 2016"
__credits__ = ["Vincenzo Marrazzo"]
__license__ = "LGPL"
__version__ = "1.0.0"
__maintainer__ = "Vincenzo Marrazzo"
__email__ = "pariamentz@gmail.com"

from Tkinter import *
from tkFont import *
from subprocess import *
from threading import Timer
import logging
import os
import sys
import time

# Session handled via UI
session_names = ['Raspbian', 'Kodi Media Center', 'Emulation Station']

default_session = 'Kodi Media Center'

emulationstation_cmd = "emulationstation"
#emulationstation_cmd = "bash -xvi emulationstation --debug 2>&1"

# Mapping of session name to sequence (of sequence) of command to execute
session_commands = {'Raspbian': [],
                    'Kodi Media Center': [["kodi-standalone"]],
                    'Emulation Station': [["sudo", "service", "lightdm", "stop"],
                                          emulationstation_cmd.split()]}


class RaspbianWelcomeGui:
    """This object handles the UI stuff of this application

        Args:
            save_on_file_stdlog (optional) : save on files the stdout/stderr of
            invoked applications
    """

    def click(self, commands):
        """Callback to handle click events"""
        logging.debug('Execute commands related session %s' % commands)
        if commands:
            execute_command_sequence(commands, self.enable_stdlog)
        logging.info("Stopping GUI")
        self.root.destroy()

    def __init__(self, save_on_file_stdlog=False):
        """Create a root Tkinter instance to contain our App"""

        self.root = Tk()
        self.enable_stdlog = save_on_file_stdlog

        logging.info('Starting GUI')

        width = 400   # width for the Tk root
        height = 320  # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.root.title("Select application")
        self.root.resizable(width=FALSE, height=FALSE)

        for session in session_names:
            button = Button(self.root,
                            font=Font(family="Helvetica", size=28),
                            text=session,
                            command=lambda argument=session_commands[session]: self.click(argument))
            button.pack(fill=BOTH, expand=1)

    def handle_event(self):
        self.root.mainloop()


def execute_command_sequence(commands_sequence, enable_stdlog=False):
    """Execute a sequence of command and handle exception"""
    for one_command in commands_sequence:
        try:
            logging.debug("Execute command '%s'" % ' '.join(one_command))

            if one_command[0] == 'sudo':
                logging.debug('Execute with sudo password')
                command_to_send = "sudo -S %s" % (' '.join(one_command[1:]))
                logging.debug("Command with sudo correction '%s'" %
                              command_to_send)
                os.popen(command_to_send, 'w').write('raspberry\n')
            else:
                #input = open('/dev/tty', 'r')
                input = None
                if enable_stdlog:
                    logging.debug('Enabled standard output/error logging')
                    now = time.strftime("%Y%m%d_%H%M%S")
                    out_filename = os.getcwd() + "/output-" + now + ".out"
                    err_filename = os.getcwd() + "/error-" + now + ".out"
                    with open(out_filename, "wb") as out, open(err_filename, "wb") as err:
                        Popen(one_command, stdin=input, stdout=out, stderr=err)
                else:
                    Popen(one_command, stdin=input)
        except OSError:
            logging.error("During command '%s'" % ' '.join(one_command))
            logging.error("Unexpected error: %s " % sys.exc_info()[1])


def main():
    """The application starts the UI on X and wait at least 60 seconds a choice.
       Passed 60 seconds it proceeds with default choice.

       Args: --debug (optional) : save on file the stdout/stderr of choiced application.
    """
    # logging related to UI functionality, enable for debug UI purpose
    # logging.basicConfig(filename='gui_execution.log',
    #                    level=logging.DEBUG,
    # format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        logging.info("Enable save on file std output/error.")
        gui = RaspbianWelcomeGui(True)
    else:
        gui = RaspbianWelcomeGui()

    # separate thread that wait 60 seconds
    # after timeout it starts kodi as default option
    commands = session_commands[default_session]
    timer = Timer(60, lambda arg=commands: [logging.debug('Timeout occurs'),
                                            gui.click(arg)])
    timer.dameon = True

    try:
        # start timer
        timer.start()

        gui.handle_event()
    finally:
        if timer.isAlive():
            logging.debug('After exit mainloop Timer is alive so cancel it')
            timer.cancel()
        else:
            logging.debug('After exit mainloop Timer is dead')

    os._exit(0)

if __name__ == '__main__':
    main()
# Copyright 2016 Vincenzo Marrazzo
