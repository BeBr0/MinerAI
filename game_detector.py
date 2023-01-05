from PIL import ImageGrab

import cell_type


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.IMAGE = ImageGrab.grab()
        self.IMAGE.save('screen.gif')

        self.X, self.Y = self.__get_border_pixel(x, y)

        self.SIZE_OF_SQUARE = self.__get_square_size()

    def detect_field(self) -> list[[int]]:
        print(f'[LOG]: Starting field detection. Square size is {self.SIZE_OF_SQUARE}')

        print(f'[LOG]: Border pixels are {self.X} {self.Y}')

        i = self.X
        j = self.Y

        field_size_x, field_size_y = self.__get_field_size()

        print(f'[LOG]: Field size is {field_size_x} {field_size_y}')
        field = []

        for ctr_i in range(field_size_x):
            field.append([])
            for ctr_j in range(field_size_y):
                cell = []
                for square_x in range(self.SIZE_OF_SQUARE):
                    for square_y in range(self.SIZE_OF_SQUARE):
                        cell.append(self.IMAGE.getpixel((i + square_x, j + square_y)))

                for cell_t in cell_type.Cell:
                    is_broken = False
                    for color in cell_t.colors:
                        if color not in cell:
                            is_broken = True
                            break

                    if not is_broken:
                        field[-1].append(cell_t.num)
                        break

            i += self.SIZE_OF_SQUARE
        j += self.SIZE_OF_SQUARE

        return field

    def __get_border_pixel(self, x: int, y: int) -> tuple[int, int]:
        i = x
        j = y

        while True:  # Detecting border
            if self.IMAGE.getpixel((i - 1, j)) != (128, 128, 128):
                i -= 1
            if self.IMAGE.getpixel((i, j - 1)) != (128, 128, 128):
                j -= 1

            if self.IMAGE.getpixel((i - 1, j)) == (128, 128, 128) and self.IMAGE.getpixel((i, j - 1)) == \
                    (128, 128, 128) and self.IMAGE.getpixel((i, j)) == (236, 236, 236):

                i -= 1
                j -= 1

                initial_i = i
                initial_j = j

                while True:
                    j -= 1

                    if self.IMAGE.getpixel((i, j - 1)) != (128, 128, 128) and self.IMAGE.getpixel((i - 1, j)) != (
                    236, 236, 236):
                        return i, j
                    if self.IMAGE.getpixel((i, j - 1)) != (128, 128, 128) or self.IMAGE.getpixel((i - 1, j)) != (
                    236, 236, 236):
                        i -= initial_i - 1
                        j -= initial_j - 1
                        break

    def __get_square_size(self) -> int:
        i = self.X
        j = self.Y

        pixel = self.IMAGE.getpixel((i, self.Y))

        size_of_square = 0

        print('pixel is ', pixel)
        if pixel == (153, 153, 153):
            print('Found closed square')
            while pixel != (255, 255, 255):  # Counting size
                size_of_square += 1

                i += 1
                pixel = self.IMAGE.getpixel((i, self.Y))

        elif pixel == (157, 157, 157):
            print('Empty or digit square found')
            while pixel != (128, 128, 128) and pixel != (255, 255, 255):
                size_of_square += 1

                i += 1
                pixel = self.IMAGE.getpixel((i, self.Y))

        return size_of_square - 1

    def __get_field_size(self) -> tuple[int, int]:
        i = self.X + self.SIZE_OF_SQUARE // 2
        j = self.Y + self.SIZE_OF_SQUARE // 2

        field_size_x = 0
        while True:
            field_size_x += 1

            i += self.SIZE_OF_SQUARE

            is_broken = True
            for index in range(self.SIZE_OF_SQUARE):
                if self.IMAGE.getpixel((i + index, j)) != (255, 255, 255):
                    is_broken = False
                    break

            if is_broken:
                break

        i = self.X + self.SIZE_OF_SQUARE // 2
        field_size_y = 0
        while True:
            field_size_y += 1

            j += self.SIZE_OF_SQUARE

            is_broken = True
            for index in range(self.SIZE_OF_SQUARE):
                if self.IMAGE.getpixel((i, j + index)) != (255, 255, 255):
                    is_broken = False
                    break

            if is_broken:
                break

        return field_size_x - 2, field_size_y - 3
