from tkinter import *
from tree import Tree
from rect import Rect,Coordinate
from renderer import TkinterRenderer

class App:
    def __init__(self, root):
        self.tree = Tree()
        self.canvas = Canvas(root, width=512, height=512, bg="white")
        self.renderer = TkinterRenderer(self.canvas)
        self.is_drawing = False
        self.mouse_hovering = False
        self.is_panning = False
        self.prev_x = 0
        self.prev_y = 0

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<ButtonPress-3>", self.on_right_down)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_up)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.canvas.pack()

        self.color = BooleanVar()
        self.color_radio_red = Radiobutton(root, text="Red", variable=self.color, value=True)
        self.color_radio_red.pack()
        self.color_radio_blue = Radiobutton(root, text="Blue", variable=self.color, value=False)
        self.color_radio_blue.pack()

        self.zoom_slider = Scale(root, from_=0,to_=8, length=300, orient="horizontal", command=self.on_zoom_changed)
        self.zoom_slider.pack()

        self.render_stats_label = Label(root)
        self.render_stats_label.pack()

    def draw(self):
        if self.is_drawing:
            self.tree.fill(self.renderer.target, self.color.get())
        self.renderer.clear()
        stats = self.tree.render(self.renderer)
        self.render_stats_label.config(
                text=f"{stats.drawn} drawn / {stats.traversed} traversed / took {stats.time*1000:.02f} ms"
            )
        if self.mouse_hovering:
            self.renderer.draw_target()

    def on_mouse_move(self, e):
        self.mouse_hovering = True
        if self.is_panning:
            dx = e.x-self.prev_x
            dy = e.y-self.prev_y
            self.renderer.move_viewport(-dx,-dy)
            self.prev_x = e.x
            self.prev_y = e.y
        self.renderer.set_target(e.x,e.y)
        self.draw()

    def on_mouse_down(self, e):
        self.is_drawing = True
        self.draw()

    def on_mouse_up(self, e):
        self.is_drawing = False

    def on_mouse_leave(self, e):
        self.mouse_hovering = False
        self.draw()

    def on_zoom_changed(self, zoom):
        self.renderer.set_viewport_zoom(-int(zoom))
        self.draw()

    def on_right_down(self, e):
        self.is_panning = True
        self.prev_x = e.x
        self.prev_y = e.y

    def on_right_up(self, e):
        self.is_panning = False

if __name__ == "__main__":
    root = Tk()
    a = App(root)
    root.mainloop()
