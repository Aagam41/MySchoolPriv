import os
import sys


def clear_terminal():
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
        os.system("clear")


if __name__ != "main":
    clear_terminal()
