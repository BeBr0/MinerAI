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

    def on_click(self, x: int, y: int, button, pressed: bool):
        if not self.called:
            self.called = True
            self.game = Game(GameField(x, y))
            self.listener.stop()
            self.stop_listener.stop()

    def on_pause(self, key):
        if key == keyboard.Key.backspace:
            self.game.is_stopped = True
            self.listener.stop()
            self.stop_listener.stop()

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
