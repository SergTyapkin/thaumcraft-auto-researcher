from typing import Union


class LinkableValue:
    def __init__(self, val: float):
        self.val = val

    def __float__(self):
        return float(self.val)

    def __int__(self):
        return int(self.val)

    def __add__(self, other):
        if isinstance(other, LinkableValue):
            return self.val + other.val
        return self.val + other

    def __sub__(self, other):
        if isinstance(other, LinkableValue):
            return self.val - other.val
        return self.val - other

    def __mul__(self, other):
        if isinstance(other, LinkableValue):
            return self.val * other.val
        return self.val * other

    def __divmod__(self, other):
        if isinstance(other, LinkableValue):
            return self.val / other.val
        return self.val / other
    # def __str__(self):
    #     return str(self.val)


class LinkableCoord:
    def __init__(self, x: float, y: float):
        self.x = LinkableValue(x)
        self.y = LinkableValue(y)
    # def __str__(self):
    #     return f'({self.x}, {self.y})'


def editLinkableValue(oldVal: Union[float, LinkableValue], newVal: float) -> Union[float, LinkableValue]:
    if isinstance(oldVal, LinkableValue):
        oldVal.val = newVal
        return oldVal
    return newVal


def linkableValueDumpsToJSON(obj):
    if isinstance(obj, LinkableValue):
        return obj.val
