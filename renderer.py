from rect import Rect, Coordinate

class TkinterRenderer:
    def __init__(self, canvas):
        self.viewport = Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0))
        self.canvas = canvas
        self.target = None
        self.zoom = 0
        self.height_hint = 0
        self.pan_cummulative_x = 0
        self.pan_cummulative_y = 0
        self.target_cursor = None

    def to_viewport_coords(self, rect):
        x1 = (rect.x1 - self.viewport.x1).shift(9).to_float()/(self.viewport.width().to_float())
        y1 = (rect.y1 - self.viewport.y1).shift(9).to_float()/(self.viewport.height().to_float())
        x2 = (rect.x2 - self.viewport.x1).shift(9).to_float()/(self.viewport.width().to_float())
        y2 = (rect.y2 - self.viewport.y1).shift(9).to_float()/(self.viewport.height().to_float())
        return [x1,y1,x2,y2]

    def clear(self):
        self.canvas.delete("all")

    def draw(self, rect, value, depth):
        [x1,y1,x2,y2] = self.to_viewport_coords(rect)
        r = int(64+(depth+1)*(255-64)/(self.height_hint))
        b = 0
        if not value:
            (r,b) = (b,r)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", fill=f"#{r:02x}00{b:02x}")
        if self.target_cursor is not None:
            self.canvas.tag_raise(self.target_cursor)

    def hint_height(self, h):
        self.height_hint = h

    def set_target(self, mx, my):
        mx = (mx // 16)*16
        my = (my // 16)*16
        self.target = Rect(
                self.viewport.x1+Coordinate(mx-32, self.zoom-9), self.viewport.y1+Coordinate(my-32, self.zoom-9),
                self.viewport.x1+Coordinate(mx+32, self.zoom-9), self.viewport.y1+Coordinate(my+32, self.zoom-9)
                )
        if self.target_cursor is not None:
            self.canvas.delete(self.target_cursor)
            self.target_cursor = None
        [x1,y1,x2,y2] = self.to_viewport_coords(self.target)
        self.target_cursor = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

    def clear_target(self):
        self.target = None
        if self.target_cursor is not None:
            self.canvas.delete(self.target_cursor)
            self.targer_cursor = None

    def set_viewport_zoom(self, e):
        self.zoom = e
        cx = (self.viewport.x1 + (self.viewport.x2-self.viewport.x1).shift(-1)).round_to(self.zoom-5)
        cy = (self.viewport.y1 + (self.viewport.y2-self.viewport.y1).shift(-1)).round_to(self.zoom-5)
        h = Coordinate(1,e-1)
        self.viewport = Rect(cx-h,cy-h,cx+h,cy+h)
        self.pan_cummulative_x = 0
        self.pan_cummulative_y = 0

    def move_viewport(self, x, y):
        self.pan_cummulative_x += x
        self.pan_cummulative_y += y
        x = self.pan_cummulative_x // 16
        if x < 0: x += 1
        y = self.pan_cummulative_y // 16
        if y < 0: y += 1
        self.pan_cummulative_x -= 16*x
        self.pan_cummulative_y -= 16*y

        self.viewport.x1 += Coordinate(x,self.zoom-5)
        self.viewport.y1 += Coordinate(y,self.zoom-5)
        self.viewport.x2 += Coordinate(x,self.zoom-5)
        self.viewport.y2 += Coordinate(y,self.zoom-5)
