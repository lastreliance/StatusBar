import time

from typing_extensions import Literal
from typing import Optional, List
from tkinter import Label, Frame

# Todo:
#  work on text height https://stackoverflow.com/questions/3950687/how-to-find-out-the-current-widget-size-in-tkinter


class StatusForm:
    def __init__(self, name="", text="", done_delay: float = 0):
        self.text = text
        self.name = name
        self.done_delay = done_delay
        self.done = 0

    def ended(self) -> bool:
        if self.done == 0:
            return False
        if (time.time() - self.done) >= self.done_delay:
            return True


class StatusBar:
    default_color = 'SystemButtonFace'

    def __init__(self, master,
                 x: int = 0,
                 y: int = 0,
                 expand: Literal["up", "down", "horizontal"] = "down",
                 row_width: int = 200,
                 height: int = 19,
                 pad_y: int = 1,
                 bg: str = "",
                 relief: Literal["raised", "sunken", "groove", "flat", "ridged", "solid"] = "groove"):
        anchor: Literal["nw", "sw"] = "nw"
        if expand == "up":
            anchor = "sw"
        if not bg:
            bg = StatusBar.default_color

        self.ycor = y
        self.pad_y = pad_y
        self.expand = expand
        self.width = row_width
        self.height = height
        self.frame = Frame(master, width=row_width, height=height)
        self.frame.pack_propagate(False)  # Stops child widgets of frame from resizing it
        self.label = Label(self.frame, anchor=anchor, bg=bg, height=1, relief=relief, justify="left", pady=pad_y)
        self.frame.place(x=x, y=y)
        self.label.pack(fill="both", expand=True)
        self.processes: List[StatusForm] = list()

        self._update()

    def set(self, name="", text="", done_delay=0, form: StatusForm = None):
        if form is not None:
            text = form.text
            name = form.name
            done_delay = form.done_delay

        text.replace("\n", " ")
        process = self.get_process(name)
        if process is None:
            self.processes.append(StatusForm(name, text, done_delay))
        else:
            process.text = text

    def get_process(self, name: str) -> Optional[StatusForm]:
        for process in self.processes:
            if process.name == name:
                return process
        return None

    def done(self, name: str, new_text=""):
        process = self.get_process(name)
        if process is None:
            return
        if process.done != 0:
            return

        process.done = time.time()
        if not new_text:
            process.text += " Success"
        else:
            process.text = new_text

    # only used once
    def _update(self):
        text = str()
        if self.expand == "down":
            for process in self.processes:
                text += process.text + "\n"
            if text.endswith("\n"):
                text = text[:-1]

        elif self.expand == "up":
            for process in self.processes:
                text = process.text + "\n" + text
            if text.endswith("\n"):
                text = text[:-1]
            displayed = len(self.label.cget("text").splitlines())
            actual = len(text.splitlines())
            if actual == 0:
                actual = 1
            if actual - displayed:
                y = self.ycor - self._get_text_height(actual)
                self.frame.place(y=y)
                print(self._get_text_height(actual))

        elif self.expand == "horizontal":
            pass

        if len(self.processes) > 1:
            for process in self.processes:
                if process.ended():
                    self.processes.remove(process)

        height = len(self.processes)
        if len(self.processes) == 0:
            height = 1
        if self.label.cget("text") != text:
            self.frame.config(height=self._get_text_height(height))
            self.label.config(text=text, height=height)
            self.label.update_idletasks()

        self.label.after(33, self._update)

    # Todo: rework
    def _get_text_height(self, rows):
        frame_height = self.height * rows
        border = self.pad_y * 2
        text_gaps = (rows - 1) * self.pad_y
        return frame_height + border - text_gaps

    def delete(self, name: str):
        for process in self.processes:
            if process.name == name:
                self.processes.remove(process)

    def destroy(self):
        self.frame.destroy()
