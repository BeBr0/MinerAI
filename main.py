import random

import pyautogui as pag
from pynput import mouse, keyboard

from game_ai import Game
from game_detector import GameField


class Main:

    def __init__(self):
        self.listener = mouse.Listener(on_click=self.on_click, suppress=False)
        self.called = False
        self.stop_listener = keyboard.Listener(on_click=self.on_pause, suppress=False)

        self.game = None
        self.wins = 0

        self.field = None

    def on_click(self, x: int, y: int, button, pressed: bool):
        if self.field is None:
            self.field = GameField(x, y)

            self.listener.stop()

            print('Отлично, поле захвачено, старайся не двигать его и не перекрывать другими окнами. '
                  'Теперь просто нажми Enter чтобы начать игру')

            input()
            Game(self.field)

    def on_pause(self, key):
        if key == keyboard.Key.backspace:
            self.game.is_stopped = True
            self.listener.stop()
            self.stop_listener.stop()

    def main(self):
        print('Привет, я ИИ, решающий игру Сапера. Чтобы начать нажми Enter: ')
        input()

        print(
            'Теперь нажми на любую клетку сапера. Не волнуйся, мины генерируются после первого нажатия :) (только '
            'в '
            'игре)')

        self.listener.start()
        self.listener.join()


if __name__ == '__main__':
    Main().main()
