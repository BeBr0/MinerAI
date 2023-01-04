from enum import Enum


class Cell(Enum):

    def __init__(self, color: tuple[int, int, int], num: int):
        self.color = color
        self.num = num

    CLOSED = ((198, 198, 198), -1)
    EMPTY = ((198, 198, 198), 0)
    ONE = ((0, 0, 255), 1)
    TWO = ((0, 128, 0), 2)
    THREE = ((255, 0, 0), 3)
    FOUR = ((0, 0, 128), 4)
    FIVE = ((128, 0, 0), 5)
