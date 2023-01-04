import time

import game_detector
from pynput import mouse


class Main:
    def __init__(self):
        self.listener = mouse.Listener(on_click=self.on_click, suppress=False)

    def on_click(self, x: int, y: int, button, pressed: bool):
        self.listener.stop()
        time.sleep(2)
        print(game_detector.detect_field(x, y))

    def main(self):
        print('Привет, я ИИ, решающий игру Сапера. Чтобы начать напиши start: ')
        inp = input()

        if inp == 'start':
            print(
                'Теперь нажми на любую клетку сапера. Не волнуйся, мины генерируются после первого нажатия :) (только '
                'в '
                'игре)')

            self.listener.start()
            self.listener.join()


if __name__ == '__main__':
    Main().main()
