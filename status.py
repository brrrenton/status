#!/usr/bin/python3

# requires "python3-pydbus" and "python3-xlib"

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


def status():
    return ''.join([' ',
                    network.ethernet_status,
                    network.wifi_status,
                    memory_free(SPACER),
                    battery.status,
                    datetime.datetime.now().strftime('%Y-%m-%d %A %-I:%M %P'),
                    ' '])


if __name__ == '__main__':

    display = Xlib.display.Display()
    root = display.screen().root

    loop = GLib.MainLoop()

    loop_thread = threading.Thread(target=loop.run)
    loop_thread.start()

    while True:
        try:
            root.set_wm_name(status())
            display.sync()
            #print(status())
            time.sleep(1)
        except KeyboardInterrupt:
            exit(0)
