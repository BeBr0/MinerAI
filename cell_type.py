from enum import Enum


class Cell(Enum):

    def __init__(self, colors: list[tuple[int, int, int]], num: int):
        self.colors = colors
        self.num = num

    CLOSED = ([(198, 198, 198), (255, 255, 255)], -1)
    EMPTY = ([(198, 198, 198), (157, 157, 157)], 0)
    ONE = ([(0, 0, 255), (157, 157, 157)], 1)
    TWO = ([(0, 128, 0), (157, 157, 157)], 2)
    THREE = ([(255, 0, 0), (157, 157, 157)], 3)
    FOUR = ([(0, 0, 128), (157, 157, 157)], 4)
    FIVE = ([(128, 0, 0), (157, 157, 157)], 5)
