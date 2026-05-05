from utils.LinkableValue import LinkableValue

class LinkableCoord:
    def __init__(self, x: float, y: float):
        self.x = LinkableValue(x)
        self.y = LinkableValue(y)
    # def __str__(self):
    #     return f'({self.x}, {self.y})'
