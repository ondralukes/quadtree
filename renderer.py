from rect import Rect, Coordinate

class TkinterRenderer:
    def __init__(self, canvas):
        self.viewport = Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0))
        self.canvas = canvas
        self.target = None
        self.height_hint = 0

    def to_viewport_coords(self, rect):
        x1 = (rect.x1 - self.viewport.x1).shift(9).to_float()/(self.viewport.width().to_float())
        y1 = (rect.y1 - self.viewport.y1).shift(9).to_float()/(self.viewport.height().to_float())
        x2 = (rect.x2 - self.viewport.x1).shift(9).to_float()/(self.viewport.width().to_float())
        y2 = (rect.y2 - self.viewport.y1).shift(9).to_float()/(self.viewport.height().to_float())
        return [x1,y1,x2,y2]

    def draw(self, rect, value, depth):
        [x1,y1,x2,y2] = self.to_viewport_coords(rect)
        r = int(128+depth*(127-64)/(self.height_hint))
        b = 0
        if not value:
            (r,b) = (b,r)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", fill=f"#{r:02x}00{b:02x}")

    def hint_height(self, h):
        self.height_hint = h

    def set_target(self, mx, my):
        mx = (mx // 16)*16
        my = (my // 16)*16
        self.target = Rect(
                Coordinate(mx-32, -9), Coordinate(my-32, -9),
                Coordinate(mx+32, -9), Coordinate(my+32,-9)
                )

    def draw_target(self):
        if self.target is None:
            return
        [x1,y1,x2,y2] = self.to_viewport_coords(self.target)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
