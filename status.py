#!/usr/bin/env python3

# DWM status bar updater
# Requires "python3-xlib"
# "Network" and "Battery" modules require "python3-pydbus"

import signal
import datetime
import Xlib.display

from gi.repository import GLib

from network import Network
from memory import memory_free
from battery import Battery

SPACER = ' | '

network = Network(SPACER)
battery = Battery(SPACER)

loop = GLib.MainLoop()

display = Xlib.display.Display()
root = display.screen().root


def status():
    return ''.join([' ',
                    network.status,
                    memory_free(SPACER),
                    battery.status,
                    datetime.datetime.now().strftime('%Y-%m-%d %A %-I:%M %P'),
                    ' '])


def handler(signum, frame):
    loop.quit()


def update():
    root.set_wm_name(status())
    display.sync()
    # print(status())
    return True


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    GLib.timeout_add_seconds(1, update)

    loop.run()
