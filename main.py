from tkinter import *
from tree import Tree
from rect import Rect,Coordinate
from renderer import TkinterRenderer
from stats_plot import StatsPlot

class App:
    def __init__(self, root):
        self.tree = Tree()
        self.canvas = Canvas(root, width=512, height=512, bg="white")
        self.renderer = TkinterRenderer(self.canvas)
        self.stats_plot_canvas = Canvas(root, width=512, height=173, bg='white')
        self.stats_plot = StatsPlot(self.stats_plot_canvas)
        self.is_drawing = False
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

        self.stats_plot_canvas.pack()

        self.color = BooleanVar()
        self.color_radio_red = Radiobutton(root, text="Red", variable=self.color, value=True)
        self.color_radio_red.pack()
        self.color_radio_blue = Radiobutton(root, text="Blue", variable=self.color, value=False)
        self.color_radio_blue.pack()

        self.zoom_slider = Scale(
                root,
                from_=0,to_=8, length=300,
                orient="horizontal", showvalue=0,
                command=self.on_zoom_changed
                )
        self.zoom_slider.pack()
        self.zoom_label = Label(root, text="Zoom: 1x")
        self.zoom_label.pack()

        self.brush_slider = Scale(
                root,
                from_=3,to_=7, length=300,
                orient="horizontal", showvalue=0,
                command=self.on_brush_changed
                )
        self.brush_slider.set(5)
        self.brush_slider.pack()
        self.brush_label = Label(root, text="Brush size: 32")
        self.brush_label.pack()


        self.render_stats_label = Label(root)
        self.render_stats_label.pack()
        self.draw()

    def draw(self):
        self.renderer.clear()
        stats = self.tree.render(self.renderer)
        self.render_stats_label.config(
                text=f"{stats.drawn} drawn ({stats.drawn_interpolated} interpolated) / {stats.traversed} traversed / took {stats.time*1000:.02f} ms"
            )
        self.stats_plot.plot(self.tree.stats)

    def on_mouse_move(self, e):
        if self.is_panning:
            dx = e.x-self.prev_x
            dy = e.y-self.prev_y
            self.renderer.move_viewport(-dx,-dy)
            self.prev_x = e.x
            self.prev_y = e.y
        if self.is_drawing and self.renderer.target is not None:
            self.tree.fill(self.renderer.target, self.color.get())
        if self.is_panning or self.is_drawing:
            self.draw()
        self.renderer.set_target(e.x,e.y)

    def on_mouse_down(self, e):
        self.is_drawing = True
        self.on_mouse_move(e)

    def on_mouse_up(self, e):
        self.is_drawing = False

    def on_mouse_leave(self, e):
        self.renderer.clear_target()

    def on_zoom_changed(self, zoom):
        z = int(zoom)
        self.renderer.set_viewport_zoom(-z)
        self.zoom_label.config(text=f"Zoom: {2**z}x")
        self.draw()

    def on_brush_changed(self, brush):
        bs = int(brush)
        self.renderer.set_brush_size(bs)
        self.brush_label.config(text=f"Brush size: {2**bs}")

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
