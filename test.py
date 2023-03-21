import time
import tkinter as tk
from threading import Thread

from statusbar import StatusBar, StatusForm


def func(status_bar, name: str, delay: float):
    def inner(bar, n, d):
        for i in range(40):
            bar.set(form=StatusForm(n, f"Task {n}:{i}"))
            time.sleep(d)

        status_bar.done(n)

    Thread(target=lambda: inner(status_bar, name, delay)).start()


def down(arg):
    func(arg, "1", 0.3)
    func(arg, "2", 0.1)


def up(arg):
    func(arg, "1", 0.1)
    func(arg, "2", 0.15)
    func(arg, "3", 0.13)


def main():
    master = tk.Tk()
    status_bar = StatusBar(master, expand="up", y=40)
    # down(status_bar)
    up(status_bar)
    # for i in range(4):
    #     status_bar.set(form=StatusForm(f"{i}", "3"))
    master.mainloop()


if __name__ == '__main__':
    main()
