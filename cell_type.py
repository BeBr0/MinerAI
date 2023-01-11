from enum import Enum


class Cell(Enum):

    def __init__(self, colors: list[tuple[int, int, int]]):
        self.colors = colors

    CLOSED = (
        [(255, 255, 255)]
    )

    EMPTY = ([])

    ONE = ([(0, 0, 255)])

    TWO = ([(75, 155, 75)])

    THREE = ([(255, 0, 0)])

    FOUR = ([(0, 0, 128)])
