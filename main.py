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
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.pack()
        self.color = BooleanVar()
        self.color_radio_red = Radiobutton(root, text="Red", variable=self.color, value=True)
        self.color_radio_red.pack()
        self.color_radio_blue = Radiobutton(root, text="Blue", variable=self.color, value=False)
        self.color_radio_blue.pack()

    def draw(self):
        if self.is_drawing:
            self.tree.fill(self.renderer.target, self.color.get())
        self.tree.render(self.renderer)
        self.renderer.draw_target()

    def on_mouse_move(self, e):
        self.renderer.set_target(e.x,e.y)
        self.draw()

    def on_mouse_down(self, e):
        self.is_drawing = True
        self.draw()

    def on_mouse_up(self, e):
        self.is_drawing = False


if __name__ == "__main__":
    root = Tk()
    a = App(root)
    root.mainloop()
