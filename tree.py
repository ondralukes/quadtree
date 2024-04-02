from rect import Rect, Coordinate

class Tree:
    def __init__(self):
        self.root = Node()
        self.root.value = False

    def fill(self, target, value):
        self.root.fill(Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)), target, value)

    def render(self, renderer):
        self.root.render(Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)), renderer)

class Node:
    def __init__(self):
        self.value = None
        self.children = [[None]*2,[None]*2]

    def fill(self, current, target, value, force_down=False):
        print(f"filling {target} with {value} current node {current}")
        if (current & target).is_empty() and not force_down:
            return

        if current in target and not force_down:
            self.value = value
            self.children = [[None]*2,[None]*2]
            return

        if self.value is not None and not force_down:
            self.fill(current, current, self.value, True)
            self.value = None

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        for dx in range(2):
            for dy in range(2):
                child_rect = Rect(current.x1+dx*halfwidth, current.y1+dy*halfheight,
                                  current.x1+(dx+1)*halfwidth, current.y1+(dy+1)*halfheight)
                if self.children[dx][dy] is None:
                    self.children[dx][dy] = Node()
                self.children[dx][dy].fill(child_rect, target, value)


    def render(self, current, renderer):
        if (current & renderer.viewport).is_empty():
            return

        if self.value is not None:
            renderer.draw(current, self.value)
            return

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        for dx in range(2):
            for dy in range(2):
                child_rect = Rect(current.x1+dx*halfwidth, current.y1+dy*halfheight,
                                  current.x1+(dx+1)*halfwidth, current.y1+(dy+1)*halfheight)
                if self.children[dx][dy] is None:
                    continue
                self.children[dx][dy].render(child_rect, renderer)

