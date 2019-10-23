#!/usr/bin/python3

from network import networks
from memory import memory_free
from battery import battery_status
import datetime

SPACER = " | "

string = networks(
    SPACER) + SPACER + "mem: " + memory_free() + SPACER + "bat: " + battery_status() + SPACER + datetime.datetime.now().strftime(
    "%Y-%m-%d %A %-I:%M %P")

print(string)
