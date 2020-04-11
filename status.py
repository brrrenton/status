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
from volume import volume
from battery import Battery

spacer = ' | '

network = Network(spacer)
battery = Battery(spacer)

loop = GLib.MainLoop()

display = Xlib.display.Display()
root = display.screen().root


def handler(signum, frame):
    loop.quit()


def status():
    return ''.join([' ',
                    network.status,
                    memory_free(spacer),
                    volume(spacer),
                    battery.status,
                    datetime.datetime.now().strftime('%Y-%m-%d %A %-I:%M %P'),
                    ' '])


def update():
    root.set_wm_name(status())
    display.sync()
    #print(status())
    return True


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    network.parent_update_function = update
    battery.parent_update_function = update

    GLib.timeout_add_seconds(1, update)

    loop.run()
