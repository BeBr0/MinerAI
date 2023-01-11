import time

from PIL import ImageGrab

import cell_type


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.field_size_cubes_x = 0
        self.field_size_cubes_y = 0

        self.field_size_x = 0
        self.field_size_y = 0

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

        y = self.Y + 1
        self.IMAGE = ImageGrab.grab(
            (self.X + 1, self.Y + 1, self.X + 1 + self.field_size_x, self.Y + 1 + self.field_size_y)
        )

        for i in range(self.field_size_cubes_x):
            field.append([])
            x = self.X + 1

            for j in range(self.field_size_cubes_y):

                current_cube = []
                for cube_x in range(self.field_size_x // self.field_size_cubes_x):
                    current_cube.append([])
                    for cube_y in range(self.field_size_y // self.field_size_cubes_y):
                        current_cube[-1].append(self.IMAGE.getpixel((x + cube_x, y + cube_y)))

                field[-1].append(self.define_cube_type(current_cube))

                x += self.field_size_x // self.field_size_cubes_x - 1

            y += self.field_size_y // self.field_size_cubes_y - 1

        print(self.cells)
        return field

    def define_cube_type(self, pixels: list[list[tuple[int, int, int]]]) -> cell_type.Cell:
        cell_pixels = []
        for cell in pixels:
            for pixel in cell:
                if pixel not in cell_pixels:
                    cell_pixels.append(pixel)

        if cell_pixels not in self.cells:
            self.cells.append(cell_pixels)

        for cell in cell_type.Cell:
            is_broken = False
            for i in range(len(pixels)):
                for j in range(len(pixels[i])):
                    if pixels[i][j] not in cell.colors:
                        is_broken = True
                        break

                if is_broken:
                    break

            if not is_broken:
                return cell

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
                current_cell = 0
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
                current_cell = 0
                self.field_size_cubes_y += 1
                self.field_size_y += 1
                y += 1

            self.field_size_y += 1
            current_cell += 1
            y += 1

        self.field_size_y -= current_cell
