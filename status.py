#!/usr/bin/python3

# requires "python3-pydbus" and "python3-xlib"

import datetime

from pydbus import SystemBus

from network import Network
from memory import memory_free
from battery import Battery

SPACER = " | "

system_bus = SystemBus()

network = Network(system_bus)
battery = Battery(system_bus)


def status():
    return "".join([" ",
                    network.ethernet(SPACER),
                    network.wifi(SPACER),
                    memory_free(SPACER),
                    battery.status(SPACER),
                    datetime.datetime.now().strftime("%Y-%m-%d %A %-I:%M %P"),
                    " "])


if __name__ == "__main__":
    import time

    import Xlib.display

    display = Xlib.display.Display()
    root = display.screen().root

    while 1:
        root.set_wm_name(status())
        display.sync()
        time.sleep(1)
