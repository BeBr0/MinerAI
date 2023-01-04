from cell_type import Cell
from PIL import ImageGrab


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y
        self.IMAGE = ImageGrab.grab()

        self.SIZE_OF_SQUARE = self.__get_square_size()

    def detect_field(self) -> list[[Cell]]:
        i, j = self.__get_border_pixel()

        field_size_x, field_size_y = self.__get_field_size()

        field = []

        i += self.SIZE_OF_SQUARE / 2
        j += self.SIZE_OF_SQUARE / 2

        for ctr_i in range(field_size_x):
            field.append([])
            for ctr_j in range(field_size_y):
                pixel = self.IMAGE.getpixel((i, j))

                for cell_type in Cell:
                    if cell_type.color == pixel:
                        field[-1].append(cell_type)
                        break

                i += self.SIZE_OF_SQUARE

            j += self.SIZE_OF_SQUARE
            i = self.X + self.SIZE_OF_SQUARE

        return field

    def __get_border_pixel(self) -> tuple[int, int]:
        i = self.X
        j = self.Y

        while True:  # Detecting border
            if self.IMAGE.getpixel((i - 1, j)) != (128, 128, 128):
                i -= 1
            if self.IMAGE.getpixel((i, j - 1)) != (128, 128, 128):
                j -= 1

            if self.IMAGE.getpixel((i - 1, j)) == (128, 128, 128) \
                    and self.IMAGE.getpixel((i, j - 1)) == (128, 128, 128):
                return i, j

    def __get_square_size(self) -> int:
        i = self.X

        pixel = self.IMAGE.getpixel((i, self.Y))

        # TODO if top of square is white count til grey, if grey, count til dark gray

        size_of_square = 0
        while pixel != (255, 255, 255):  # Counting size
            size_of_square += 1

            i += 1
            pixel = self.IMAGE.getpixel((i, self.Y))

        return size_of_square

    def __get_field_size(self) -> tuple[int, int]:
        i = self.X + self.SIZE_OF_SQUARE
        j = self.Y + self.SIZE_OF_SQUARE

        pixel = self.IMAGE.getpixel((i, j))

        field_size_x = 0
        while pixel != (255, 255, 255):
            field_size_x += 1

            i += self.SIZE_OF_SQUARE / 2
            pixel = self.IMAGE.getpixel((i, j))

        i = self.X + self.SIZE_OF_SQUARE
        field_size_y = 0
        while pixel != (255, 255, 255):
            field_size_y += 1

            j += self.SIZE_OF_SQUARE / 2
            pixel = self.IMAGE.getpixel((i, j))

        return field_size_x - 2, field_size_y - 2
