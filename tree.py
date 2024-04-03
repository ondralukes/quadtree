from rect import Rect, Coordinate

class Tree:
    def __init__(self):
        self.stats = TreeStats()
        self.root = Node(self.stats, 0)
        self.root.value = False

    def fill(self, target, value):
        self.root.fill(
                Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)),
                target, value, self.stats, 0)

    def render(self, renderer):
        renderer.hint_height(self.stats.get_height())
        self.root.render(Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)), renderer, 0)

class TreeStats:
    def __init__(self):
        self.counts = [0]

    def add(self, depth):
        while len(self.counts) <= depth:
            self.counts.append(0)
        self.counts[depth] += 1

    def remove(self, depth):
        self.counts[depth] -= 1
        while self.counts[-1] == 0:
            self.counts.pop()

    def get_height(self):
        return len(self.counts)

class Node:
    def __init__(self, stats, depth):
        self.value = None
        self.children = [[None]*2,[None]*2]
        stats.add(depth)

    def fill(self, current, target, value, stats, depth, force_down=False):
        if (current & target).is_empty():
            return

        if current in target and not force_down:
            self.value = value
            self.log_remove(stats, depth, False)
            self.children = [[None]*2,[None]*2]
            return

        if self.value == value and not force_down:
            return

        if self.value is not None and not force_down:
            self.fill(current, current, self.value, stats, depth, True)
        self.value = None

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        common_cnt = 0
        common_value = None
        for dx in range(2):
            for dy in range(2):
                child_rect = Rect(current.x1+dx*halfwidth, current.y1+dy*halfheight,
                                  current.x1+(dx+1)*halfwidth, current.y1+(dy+1)*halfheight)
                if self.children[dx][dy] is None:
                    self.children[dx][dy] = Node(stats, depth+1)
                self.children[dx][dy].fill(child_rect, target, value, stats, depth+1)
                if self.children[dx][dy].value == common_value:
                    common_cnt += 1
                else:
                    common_value = self.children[dx][dy].value
                    common_cnt = 1
        if common_value != None and common_cnt == 4 and not force_down:
            self.value = common_value
            self.log_remove(stats, depth, False)
            self.children = [[None]*2,[None]*2]


    def render(self, current, renderer, depth):
        if (current & renderer.viewport).is_empty():
            return

        if self.value is not None:
            renderer.draw(current, self.value, depth)
            return

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        for dx in range(2):
            for dy in range(2):
                child_rect = Rect(current.x1+dx*halfwidth, current.y1+dy*halfheight,
                                  current.x1+(dx+1)*halfwidth, current.y1+(dy+1)*halfheight)
                if self.children[dx][dy] is None:
                    continue
                self.children[dx][dy].render(child_rect, renderer, depth+1)

    def log_remove(self, stats, depth, include_self):
        for dx in range(2):
            for dy in range(2):
                if self.children[dx][dy] is None:
                    continue
                self.children[dx][dy].log_remove(stats, depth+1, True)
        if include_self:
            stats.remove(depth)
