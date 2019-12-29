#!/usr/bin/env python3

# DWM status bar updater
# Requires "python3-xlib"
# "Network" and "Battery" modules require "python3-pydbus"

import signal
import time
import datetime
import threading
import Xlib.display

from gi.repository import GLib

from network import Network
from memory import memory_free
from battery import Battery

SPACER = ' | '

network = Network(SPACER)
battery = Battery(SPACER)

loop = GLib.MainLoop()
loop_thread = threading.Thread(target=loop.run)

display = Xlib.display.Display()
root = display.screen().root

interrupted = False


def status():
    return ''.join([' ',
                    network.status,
                    memory_free(SPACER),
                    battery.status,
                    datetime.datetime.now().strftime('%Y-%m-%d %A %-I:%M %P'),
                    ' '])


def handler(signum, frame):
    global interrupted
    interrupted = True
    loop.quit()


if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)

    loop_thread.start()

    while not interrupted:
        root.set_wm_name(status())
        display.sync()
        time.sleep(1)
