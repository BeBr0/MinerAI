import pyautogui


def take_screenshot(x1: int, y1: int, x2: int, y2: int):
    screenshot = pyautogui.screenshot(region=(x1, y1, x2, y2))
    return screenshot


def detect_field(x: int, y: int):
    screenshot = take_screenshot(x-50, y-50, x+50, y+50)
    screenshot.save("screenshot.png")
