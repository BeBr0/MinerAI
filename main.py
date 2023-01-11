import time

from game_detector import GameField
from pynput import mouse, keyboard
from game_ai import Game


class Main:
    def __init__(self):
        self.listener = mouse.Listener(on_click=self.on_click, suppress=False)
        self.stop_listener = keyboard.Listener(on_press=self.program_stop_listener, suppress=False)
        self.called = False

        self.game = None

    def on_click(self, x: int, y: int, button, pressed: bool):
        self.listener.stop()

        if not self.called:
            self.called = True
            self.game = Game(GameField(x, y))

            self.stop_listener.stop()

    def program_stop_listener(self, key):
        if key == keyboard.Key.backspace:
            self.game.is_stopped = True

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
            self.stop_listener.start()
            self.stop_listener.join()


if __name__ == '__main__':
    Main().main()
