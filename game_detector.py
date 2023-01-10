from PIL import ImageGrab


class FieldDetector:

    def __init__(self, x: int, y: int):
        self.field_size_x = 0
        self.field_size_y = 0
        self.IMAGE = ImageGrab.grab()
        self.X = x
        self.Y = y

    def detect_field(self) -> list[[int]]:
        self.find_top_left()
        print(f'found border at {self.X} {self.Y}')

        self.get_field_sizes()

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

        while self.IMAGE.getpixel((x, y)) != (198, 198, 198):
            if (self.IMAGE.getpixel((x, y)) == (192, 192, 192) and self.IMAGE.getpixel((x + 1, y)) == (
                    128, 128, 128)) or self.IMAGE.getpixel((x, y)) == (128, 128, 128):
                self.field_size_x += 1
                x += 1

            x += 1

        x = self.X + 2
        y = self.Y + 2
        while self.IMAGE.getpixel((x, y)) != (198, 198, 198):
            if (self.IMAGE.getpixel((x, y)) == (192, 192, 192) and self.IMAGE.getpixel((x + 1, y)) == (
                    128, 128, 128)) or self.IMAGE.getpixel((x, y)) == (128, 128, 128):
                self.field_size_y += 1
                y += 1

            y += 1
