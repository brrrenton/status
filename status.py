#!/usr/bin/python3

# requires "python3-pydbus" and "python3-xlib"

import time
import datetime

from pydbus import SystemBus

from network import Network
from memory import memory_free
from battery import Battery

import Xlib.display

display = Xlib.display.Display()
root = display.screen().root

SPACER = " | "

system_bus = SystemBus()

network = Network(system_bus)
battery = Battery(system_bus)

while 1:
    string = "".join([" ",
                      network.ethernet(SPACER),
                      network.wifi(SPACER),
                      memory_free(SPACER),
                      battery.status(SPACER),
                      datetime.datetime.now().strftime("%Y-%m-%d %A %-I:%M %P"),
                      " "])

    root.set_wm_name(string)
    display.sync()
    time.sleep(1)
