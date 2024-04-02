from rect import Rect, Coordinate

class TkinterRenderer:
    def __init__(self, canvas):
        self.viewport = Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0))
        self.canvas = canvas

    def draw(self, rect, value):
        x1 = 500*(rect.x1 - self.viewport.x1).to_float()/(self.viewport.width().to_float())
        y1 = 500*(rect.y1 - self.viewport.y1).to_float()/(self.viewport.height().to_float())
        x2 = 500*(rect.x2 - self.viewport.x1).to_float()/(self.viewport.width().to_float())
        y2 = 500*(rect.y2 - self.viewport.y1).to_float()/(self.viewport.height().to_float())
        print(f"draw {value} to canvas ({x1},{y1}),({x2},{y2})")
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', fill='black' if value else 'white')
