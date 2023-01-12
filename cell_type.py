from enum import Enum


class Cell(Enum):

    def __init__(self, colors: list[tuple[int, int, int]], num: int):
        self.colors = colors
        self.num = num

    CLOSED = ([(255, 255, 255)], -2)

    EMPTY = ([], -1)

    FLAG = ([], 0)

    ONE = ([(0, 0, 255)], 1)

    TWO = ([(75, 155, 75)], 2)

    THREE = ([(255, 0, 0)], 3)

    FOUR = ([(0, 0, 128)], 4)

    FIVE = ([(128, 0, 0)], 5)
