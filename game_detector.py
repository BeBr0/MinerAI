import time

from PIL import ImageGrab

import cell_type


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.field_size_cubes_x = 0
        self.field_size_cubes_y = 0

        self.field_size_x = 0
        self.field_size_y = 0

        self.cubes = [[], []]

        self.IMAGE = ImageGrab.grab()
        self.X = x
        self.Y = y

        self.cells = []

    def detect_field(self) -> list[[int]]:
        self.find_top_left()
        print(f'found border at {self.X} {self.Y}')

        self.get_field_sizes()

        print(f'Field sizes in cubes: {self.field_size_cubes_x} {self.field_size_cubes_y}'
              f'\nField sizes in pixels: {self.field_size_x} {self.field_size_y}')

        time.sleep(1)
        field = []

        self.IMAGE = ImageGrab.grab(
            (self.X + 1, self.Y + 1, self.X + 1 + self.field_size_x, self.Y + 1 + self.field_size_y)
        )

        self.X = 0
        self.Y = 0

        self.IMAGE.save('screen.png')

        x = 0
        y = 0

        sum_x = 0
        sum_y = 0
        for j in range(len(self.cubes[1])):
            field.append([])

            sum_x = 0
            for i in range(len(self.cubes[0])):

                pixels = []
                for cube_y in range(1, self.cubes[1][j] - 1):
                    pixels.append([])

                    for cube_x in range(1, self.cubes[0][i] - 1):
                        pixels[-1].append(self.IMAGE.getpixel((sum_x + cube_x, sum_y + cube_y)))

                field[-1].append(self.define_cube_type(pixels))

                sum_x += self.cubes[0][i]
            sum_y += self.cubes[1][j]

        return field

    def define_cube_type(self, pixels: list[list[tuple[int, int, int]]]) -> cell_type.Cell:
        for cell in cell_type.Cell:
            if cell is not cell_type.Cell.CLOSED or cell is not cell_type.Cell.EMPTY:
                for i in range(len(pixels)):
                    for j in range(len(pixels[i])):
                        if pixels[i][j] in cell.colors:
                            return cell

        if (255, 255, 255) in pixels:
            return cell_type.Cell.CLOSED
        else:
            return cell_type.Cell.EMPTY

    def find_top_left(self):
        i = self.X
        j = self.Y

        while True:
            is_border = True
            for num in range(0, 4):
                if self.IMAGE.getpixel((i - num, j)) != (128, 128, 128):
                    is_border = False

            if is_border:
                break

            i -= 1

        while self.IMAGE.getpixel((i + 1, j)) == (128, 128, 128):
            i += 1

        while self.IMAGE.getpixel((i + 1, j)) != (128, 128, 128):
            j -= 1

        self.X = i
        self.Y = j

    def get_field_sizes(self):
        x = self.X + 2
        y = self.Y + 2

        current_cell = 2
        self.field_size_x = 2
        while self.IMAGE.getpixel((x, y)) != (198, 198, 198) or self.IMAGE.getpixel((x + 1, y)) != (198, 198, 198):

            if self.IMAGE.getpixel((x, y)) == (192, 192, 192) or (self.IMAGE.getpixel((x, y)) == (
                    186, 186, 186) and self.IMAGE.getpixel((x + 1, y)) == (128, 128, 128)):
                self.cubes[0].append(current_cell)

                current_cell = 1
                self.field_size_cubes_x += 1
                self.field_size_x += 1
                x += 1

            self.field_size_x += 1
            current_cell += 1
            x += 1

        self.field_size_x -= current_cell

        x = self.X + 2
        y = self.Y + 2

        current_cell = 2
        self.field_size_y = 2

        while self.IMAGE.getpixel((x, y)) != (198, 198, 198) or self.IMAGE.getpixel((x, y + 1)) != (198, 198, 198):

            if self.IMAGE.getpixel((x, y)) == (192, 192, 192) or (self.IMAGE.getpixel((x, y)) == (
                    186, 186, 186) and self.IMAGE.getpixel((x, y + 1)) == (128, 128, 128)):
                self.cubes[1].append(current_cell)

                current_cell = 1
                self.field_size_cubes_y += 1
                self.field_size_y += 1
                y += 1

            self.field_size_y += 1
            current_cell += 1
            y += 1

        self.field_size_y -= current_cell
