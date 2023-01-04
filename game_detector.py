from cell_type import Cell
from PIL import ImageGrab


def detect_field(x: int, y: int) -> list[[Cell]]:
    i = x
    j = y
    image = ImageGrab.grab()  # Create image
    while True:  # Detecting border
        if image.getpixel((i - 1, j)) != (128, 128, 128):
            i -= 1
        if image.getpixel((i, j - 1)) != (128, 128, 128):
            j -= 1

        if image.getpixel((i - 1, j)) == (128, 128, 128) and image.getpixel((i, j - 1)) == (128, 128, 128):
            break

    field_start_x = i
    field_start_y = j

    field_size_x = 0
    field_size_y = 0

    size_of_square = 0

    pixel = image.getpixel((i, j))
    while pixel != (255, 255, 255):  # Counting size
        size_of_square += 1

        i += 1
        pixel = image.getpixel((i, j))

    i = field_start_x
    print(size_of_square)
    i += size_of_square / 2
    j += size_of_square / 2
    pixel = image.getpixel((i, j))
    while pixel != (255, 255, 255):
        field_size_x += 1

        i += size_of_square / 2
        pixel = image.getpixel((i, j))

    field_size_x -= 1
    i = field_size_x
    field_size_x_pixels = i - field_start_x

    pixel = image.getpixel((i, j))
    while pixel != (255, 255, 255):
        field_size_y += 1

        j += size_of_square / 2
        pixel = image.getpixel((i, j))

    field_size_y_pixels = j - field_start_y

    field_size_y -= 1
    j = field_start_y

    field = []

    initial_i = i
    initial_j = j

    i += size_of_square / 2
    j += size_of_square / 2

    print(field_size_x, field_size_y)
    for ctr_i in range(field_size_x):
        field.append([])
        for ctr_j in range(field_size_y):
            pixel = image.getpixel((i, j))

            for cell_type in Cell:
                if cell_type.color == pixel:
                    field[-1].append(cell_type)
                    break
            i += size_of_square

        j += size_of_square
        i = initial_i + size_of_square

    return field
