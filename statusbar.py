import time

from typing_extensions import Literal
from typing import Optional, List
from tkinter import Label, Frame


class StatusForm:
    def __init__(self, name="", text="", done_delay: float = 2):
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
                 width: int = 200,
                 height: int = 20,
                 bg: str = "",
                 relief: Literal["raised", "sunken", "groove", "flat", "ridged", "solid"] = "groove"):
        anchor: Literal["nw", "sw"] = "nw"
        if expand == "up":
            anchor = "sw"
        if not bg:
            bg = StatusBar.default_color
        self.expand = expand
        self.width = width
        self.height = height
        self.frame = Frame(master, width=width, height=height)
        self.frame.pack_propagate(False)  # Stops child widgets of frame from resizing it
        self.label = Label(self.frame, anchor=anchor, bg=bg, height=1, relief=relief)
        self.frame.place(x=x, y=y)
        self.label.pack(fill="both", expand=True)
        self.processes: List[StatusForm] = list()

        self._update()

    def set(self, form: StatusForm):
        form.text.replace("\n", " ")
        process = self.get_process(form.name)
        if process is None:
            self.processes.append(form)
        else:
            process.text = form.text

    def get_process(self, name: str) -> Optional[StatusForm]:
        for process in self.processes:
            if process.name == name:
                return process
        return None

    def _set_frame_size(self, rows):
        pass

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
            # TODO: algorithm to adjust the height
            self._set_frame_size(1)
            pass
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
            self.frame.config(height=height * self.height)
            self.label.config(text=text, height=height)
            self.label.update_idletasks()

        self.label.after(33, self._update)

    def delete(self, name: str):
        for process in self.processes:
            if process.name == name:
                self.processes.remove(process)

    def destroy(self):
        self.frame.destroy()
