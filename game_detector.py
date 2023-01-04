import pyautogui


def detect_field(x: int, y: int):
    for i in range(x, x+100):
        for j in range(y, y+100):
            pixel = pyautogui.pixel(i, j)


