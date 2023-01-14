import time

import pyautogui as pag
from PIL import ImageGrab

import cell_type


def define_cube_type(pixels: list[list[tuple[int, int, int]]]) -> cell_type.Cell:

    for row in pixels:
        if (0, 0, 0) in row:
            return cell_type.Cell.BOMB
        elif (255, 255, 255) in row:
            return cell_type.Cell.CLOSED

    for cell in cell_type.Cell:
        if cell is not cell_type.Cell.CLOSED and cell is not cell_type.Cell.EMPTY:
            for i in range(len(pixels)):
                for j in range(len(pixels[i])):
                    if pixels[i][j] in cell.colors:
                        return cell

    return cell_type.Cell.EMPTY


class GameField:

    def __init__(self, x: int, y: int):
        self.IMAGE = ImageGrab.grab()

        self.field_array: list[list[cell_type.Cell]] = []
        self.field_size_cubes_x = 0
        self.field_size_cubes_y = 0

        self.field_size_x = 0
        self.field_size_y = 0

        self.__cubes = [[], []]

        self.__X = x
        self.__Y = y

        self.field_start_x = 0
        self.field_start_y = 0

        time.sleep(1)

        self.detect_field()

    def detect_field(self):
        self.__find_top_left()
        print(f'found border at {self.field_start_x} {self.field_start_y}')

        self.__get_field_sizes()

        print(f'Field sizes in cubes: {self.field_size_cubes_x} {self.field_size_cubes_y}'
              f'\nField sizes in pixels: {self.field_size_x} {self.field_size_y}')

        self.__build_field()

    def put(self, x: int, y: int, cell: cell_type.Cell):
        sum_x = 0
        sum_y = 0
        for i in range(y):
            sum_x += self.__cubes[0][i]

        for i in range(x):
            sum_y += self.__cubes[1][i]

        if cell == cell_type.Cell.FLAG:
            pag.click(x=self.field_start_x + sum_x + 2, y=self.field_start_y + sum_y + 2, button='SECONDARY')
        elif cell == cell_type.Cell.EMPTY:
            pag.click(x=self.field_start_x + sum_x + 2, y=self.field_start_y + sum_y + 2, button='PRIMARY')

    def update_field(self) -> bool:
        self.IMAGE = ImageGrab.grab((
            self.field_start_x,
            self.field_start_y,
            self.field_start_x + 1 + self.field_size_x,
            self.field_start_y + 1 + self.field_size_y
        ))

        sum_y = 0
        result = False
        for j in range(len(self.__cubes[1])):

            sum_x = 0
            for i in range(len(self.__cubes[0])):

                if self.field_array[j][i] == cell_type.Cell.CLOSED:

                    pixels = []
                    for cube_y in range(1, self.__cubes[1][j] - 1):
                        pixels.append([])

                        for cube_x in range(1, self.__cubes[0][i] - 1):
                            pixels[-1].append(self.IMAGE.getpixel((sum_x + cube_x, sum_y + cube_y)))

                    self.field_array[j][i] = define_cube_type(pixels)

                    if self.field_array[j][i] == cell_type.Cell.BOMB:
                        result = True

                sum_x += self.__cubes[0][i]
            sum_y += self.__cubes[1][j]

        return result

    def __build_field(self):
        self.IMAGE = ImageGrab.grab(
            (self.__X + 1, self.__Y + 1, self.__X + 1 + self.field_size_x, self.__Y + 1 + self.field_size_y)
        )

        self.__X = 0
        self.__Y = 0

        sum_y = 0
        for j in range(len(self.__cubes[1])):
            self.field_array.append([])

            sum_x = 0
            for i in range(len(self.__cubes[0])):

                pixels = []
                for cube_y in range(1, self.__cubes[1][j] - 1):
                    pixels.append([])

                    for cube_x in range(1, self.__cubes[0][i] - 1):
                        pixels[-1].append(self.IMAGE.getpixel((sum_x + cube_x, sum_y + cube_y)))

                self.field_array[-1].append(define_cube_type(pixels))

                sum_x += self.__cubes[0][i]
            sum_y += self.__cubes[1][j]

    def __find_top_left(self):
        i = self.__X
        j = self.__Y

        while True:
            is_border = True
            for num in range(0, 6):
                if self.IMAGE.getpixel((i - num, j)) != (128, 128, 128):
                    is_border = False

            if is_border:
                break

            i -= 1

        while self.IMAGE.getpixel((i + 1, j)) == (128, 128, 128):
            i += 1

        while self.IMAGE.getpixel((i + 1, j)) != (128, 128, 128):
            j -= 1

        self.__X = i
        self.__Y = j

        self.field_start_x = i + 1
        self.field_start_y = j + 1

    def __get_field_sizes(self):
        x = self.__X + 2
        y = self.__Y + 2

        current_cell = 2
        self.field_size_x = 2
        while self.IMAGE.getpixel((x, y)) != (198, 198, 198) or self.IMAGE.getpixel((x + 1, y)) != (198, 198, 198):

            if self.IMAGE.getpixel((x, y)) == (192, 192, 192) or ((self.IMAGE.getpixel((x, y)) == (
                    186, 186, 186) or self.IMAGE.getpixel((x, y)) == (191, 191, 191)) and self.IMAGE.getpixel((x + 1, y)) == (128, 128, 128)):
                self.__cubes[0].append(current_cell)

                current_cell = 1
                self.field_size_cubes_x += 1
                self.field_size_x += 1
                x += 1

            self.field_size_x += 1
            current_cell += 1
            x += 1

            # Сделать чтобы было не равно 255

        self.field_size_x -= current_cell

        x = self.__X + 2
        y = self.__Y + 2

        current_cell = 2
        self.field_size_y = 2

        while self.IMAGE.getpixel((x, y)) != (198, 198, 198) or self.IMAGE.getpixel((x, y + 1)) != (198, 198, 198):

            if self.IMAGE.getpixel((x, y)) == (192, 192, 192) or ((self.IMAGE.getpixel((x, y)) == (
                    186, 186, 186) or self.IMAGE.getpixel((x, y)) == (191, 191, 191)) and self.IMAGE.getpixel((x, y + 1)) == (128, 128, 128)):
                self.__cubes[1].append(current_cell)

                current_cell = 1
                self.field_size_cubes_y += 1
                self.field_size_y += 1
                y += 1

            self.field_size_y += 1
            current_cell += 1
            y += 1

        self.field_size_y -= current_cell
