import time

from game_detector import FieldDetector
from pynput import mouse


class Main:
    def __init__(self):
        self.listener = mouse.Listener(on_click=self.on_click, suppress=False)
        self.called = False

    def on_click(self, x: int, y: int, button, pressed: bool):
        self.listener.stop()

        if not self.called:
            self.called = True
            field = FieldDetector(x, y).detect_field()

            for row in field:
                for item in row:
                    print(item, end=' ')
                print()

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
