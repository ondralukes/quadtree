from tkinter import *
from tree import Tree
from rect import Rect,Coordinate
from renderer import TkinterRenderer

if __name__ == "__main__":
    t = Tree()
    t.fill(Rect(Coordinate(1,-2), Coordinate(2,-2), Coordinate(3,-2), Coordinate(1,0)), True)
    t.fill(Rect(Coordinate(12,-5), Coordinate(10,-4), Coordinate(13,-5), Coordinate(11,-4)), False)
    root = Tk()
    canvas = Canvas(root, width=500, height=500, bg="white")
    canvas.pack()
    renderer = TkinterRenderer(canvas)
    t.render(renderer)
    root.mainloop()
