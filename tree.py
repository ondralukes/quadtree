from rect import Rect, Coordinate
import time

class Tree:
    def __init__(self):
        self.stats = TreeStats()
        self.root = Node(self.stats, 0)
        self.root.value = False
        self.leaf_areas = [Coordinate(1,0), Coordinate(0, 0)]
        self.stats.add_leaf(0, False)

    def fill(self, target, value):
        self.root.fill(
                Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)),
                target, value, self.stats, 0)

    def render(self, renderer):
        renderer.hint_height(self.stats.get_height())
        stats = RenderStats()
        stats.start_stopwatch()
        self.root.render(Rect(Coordinate(0,0), Coordinate(0,0), Coordinate(1,0), Coordinate(1,0)), renderer, 0, stats)
        stats.stop_stopwatch()
        return stats

class RenderStats:
    def __init__(self):
        self.traversed = 0
        self.drawn = 0
        self.drawn_interpolated = 0

    def start_stopwatch(self):
        self.time = time.perf_counter()

    def stop_stopwatch(self):
        self.time = time.perf_counter()-self.time

class TreeStats:
    def __init__(self):
        self.counts = [0]
        self.leaf_counts = [[0],[0]]

    def add(self, depth):
        while len(self.counts) <= depth:
            self.counts.append(0)
        self.counts[depth] += 1

    def remove(self, depth):
        self.counts[depth] -= 1
        while self.counts[-1] == 0:
            self.counts.pop()

    def add_leaf(self, depth, value):
        v = 1 if value else 0
        while len(self.leaf_counts[v]) <= depth:
            self.leaf_counts[v].append(0)
        self.leaf_counts[v][depth] += 1

    def remove_leaf(self, depth, value):
        v = 1 if value else 0
        self.leaf_counts[v][depth] -= 1
        while len(self.leaf_counts[v]) != 0 and self.leaf_counts[v][-1] == 0:
            self.leaf_counts[v].pop()

    def get_height(self):
        return len(self.counts)

    def get_leaf_count(self, depth, value):
        v = 1 if value else 0
        if len(self.leaf_counts[v]) <= depth:
            return 0
        return self.leaf_counts[v][depth]


class Node:
    def __init__(self, stats, depth):
        self.value = None
        self.children = [[None]*2,[None]*2]
        stats.add(depth)
        self.leaf_areas = [Coordinate(0,0), Coordinate(0,0)]

    def fill(self, current, target, value, stats, depth, force_down=False):
        if (current & target).is_empty():
            return

        if current in target and not force_down:
            if self.value is not None:
                stats.remove_leaf(depth, self.value)
            self.value = value
            if self.value:
                self.leaf_areas = [Coordinate(0,0), Coordinate(1, -2*depth)]
            else:
                self.leaf_areas = [Coordinate(1, -2*depth), Coordinate(0,0)]
            stats.add_leaf(depth, self.value)
            self.log_remove(stats, depth, False)
            self.children = [[None]*2,[None]*2]
            return

        if self.value == value and not force_down:
            return

        if self.value is not None and not force_down:
            self.fill(current, current, self.value, stats, depth, True)

        if self.value is not None:
            stats.remove_leaf(depth, self.value)
        self.value = None

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        common_cnt = 0
        common_value = None
        self.leaf_areas = [Coordinate(0,0), Coordinate(0,0)]
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
                self.leaf_areas[0] += self.children[dx][dy].leaf_areas[0]
                self.leaf_areas[1] += self.children[dx][dy].leaf_areas[1]
        if common_value != None and common_cnt == 4 and not force_down:
            self.value = common_value
            if self.value:
                self.leaf_areas = [Coordinate(0,0), Coordinate(1, -2*depth)]
            else:
                self.leaf_areas = [Coordinate(1, -2*depth), Coordinate(0,0)]
            stats.add_leaf(depth, self.value)
            self.log_remove(stats, depth, False)
            self.children = [[None]*2,[None]*2]


    def render(self, current, renderer, depth, stats):
        stats.traversed += 1
        if (current & renderer.viewport).is_empty():
            return

        if self.value is not None:
            stats.drawn += 1
            renderer.draw(current, self.value, depth)
            return

        if depth == renderer.get_max_depth():
            stats.drawn += 1
            stats.drawn_interpolated += 1
            renderer.draw(current, self.leaf_areas[1] > self.leaf_areas[0], depth)
            return

        halfwidth = current.width().shift(-1)
        halfheight = current.height().shift(-1)
        for dx in range(2):
            for dy in range(2):
                child_rect = Rect(current.x1+dx*halfwidth, current.y1+dy*halfheight,
                                  current.x1+(dx+1)*halfwidth, current.y1+(dy+1)*halfheight)
                if self.children[dx][dy] is None:
                    continue
                self.children[dx][dy].render(child_rect, renderer, depth+1, stats)

    def log_remove(self, stats, depth, include_self):
        for dx in range(2):
            for dy in range(2):
                if self.children[dx][dy] is None:
                    continue
                self.children[dx][dy].log_remove(stats, depth+1, True)
        if include_self:
            stats.remove(depth)
            if self.value is not None:
                stats.remove_leaf(depth, self.value)
