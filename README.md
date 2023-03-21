# StatusBar
## version - 0.3
## A tkinter module to present a status bar in app.

### Usage:
``` rb
root = Tk()
status_bar = StatusBar(root, x=0, y=0, expand="down", width=200, height=12, bg="yellow")
status_bar.set(StatusForm(name="name1", text="loading...", done_delay=3))
status_bar.set(StatusForm(name="name1", text="loaded!"))
status_bar.done(name="name1")
status_bar.destroy()
```
