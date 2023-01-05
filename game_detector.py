from cell_type import Cell
from PIL import ImageGrab
import turtle


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.IMAGE = ImageGrab.grab()
        self.IMAGE.save('screen.gif')

        self.X, self.Y = self.__get_border_pixel(x, y)
        # self.turtle = turtle.Turtle()
        # self.screen = turtle.Screen()
        # self.screen.addshape('screen.gif')
        # self.turtle.shape('screen.gif')

        self.SIZE_OF_SQUARE = self.__get_square_size()

    def detect_field(self) -> list[[Cell]]:
        print(f'[LOG]: Starting field detection. Square size is {self.SIZE_OF_SQUARE}')

        print(f'[LOG]: Border pixels are {self.X} {self.Y}')

        i = self.X
        j = self.Y

        # self.turtle.penup()
        # self.turtle.speed(1)
        # self.turtle.goto(i, j)
        # self.turtle.pendown()

        # print('dot')
        # self.turtle.dot(3, (255, 3, 3))

        field_size_x, field_size_y = self.__get_field_size()

        print(f'[LOG]: Field size is {field_size_x} {field_size_y}')
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

    def __get_border_pixel(self, x: int, y: int) -> tuple[int, int]:
        i = x
        j = y

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
        i = self.X - 1 + self.SIZE_OF_SQUARE // 2
        j = self.Y - 1 + self.SIZE_OF_SQUARE // 2

        pixel = self.IMAGE.getpixel((i, j))

        field_size_x = 0
        while pixel != (255, 255, 255):
            field_size_x += 1

            i += self.SIZE_OF_SQUARE
            pixel = self.IMAGE.getpixel((i, j))

        i = self.X + self.SIZE_OF_SQUARE // 2
        field_size_y = 0
        while pixel != (255, 255, 255):
            field_size_y += 1

            j += self.SIZE_OF_SQUARE
            pixel = self.IMAGE.getpixel((i, j))

        return field_size_x - 1, field_size_y - 1
