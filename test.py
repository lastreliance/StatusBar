import time
import tkinter as tk
from threading import Thread

from statusbar import StatusBar, StatusForm


def a(status_bar):
    for i in range(30):
        status_bar.set(StatusForm("1", f"Task 1:{i}"))
        time.sleep(0.15)

    status_bar.done("1")


def c(status_bar):
    for i in range(40):
        status_bar.set(StatusForm("2", f"Task 2:{i}"))
        time.sleep(0.1)

    status_bar.done("2")


def b(arg):
    start(a, arg)
    start(c, arg)



def start(func, arg):
    Thread(target=lambda: func(arg)).start()


def main():
    master = tk.Tk()
    status_bar = StatusBar(master)
    b(status_bar)
    master.mainloop()


if __name__ == '__main__':
    main()
