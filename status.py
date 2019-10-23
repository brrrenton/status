#!/usr/bin/python3

from network import networks
from memory import memory_free

SPACER = " | "

string = networks(SPACER) + SPACER + "mem: " + memory_free()

print(string)
