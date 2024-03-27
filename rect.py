from functools import total_ordering

@total_ordering
class Coordinate:
    """
    Represents a number of the form p*2^e
    """
    def __init__(self, p, e):
        while p % 2 == 0:
            p //= 2
            e += 1
        self.e = e
        self.p = p

    def __add__(self, other):
        if self.e <= other.e:
            return Coordinate(self.p + other.p*(2**(other.e-self.e)), self.e)
        return Coordinate(other.p + self.p*(2**(self.e-other.e)), other.e)

    def __sub__(self, other):
        return self + -1*other

    def __gt__(self, other):
        if self.e <= other.e:
            return self.p > other.p*(2**(other.e-self.e))
        return other.p < self.p*(2**(other.e-self.e))

    def __eq__(self, other):
        return self.e == other.e and self.p == other.p

    def __mul__(self, t):
        return Coordinate(self.p*t, self.e)

    def __rmul__(self, t):
        return Coordinate(self.p*t, self.e)

    def __repr__(self):
        return f"{self.p}*2^({self.e})"


class Rect:
    """
    Represents a rectangle
    """
    def __init__(self, x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __contains__(self, other):
        return self.x1 <= other.x1 and other.x2 <= self.x2 \
            and self.y1 <= other.y1 and other.y2 <= self.y2

    def __and__(self, other):
        return Rect(max(self.x1,other.x1), max(self.y1, other.y1),
            min(self.x2, other.x2), min(self.y2, other.y2))

    def is_empty(self):
        return self.x1 >= self.x2 or self.y1 >= self.y2
