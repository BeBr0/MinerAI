import copy
import time

import pyautogui as pag
from pynput import mouse, keyboard

import cell_type
from game_ai import Game
from game_detector import GameField


class Main:

    def __init__(self):
        self.listener = mouse.Listener(on_click=self.on_click, suppress=False)
        self.called = False
        self.stop_listener = keyboard.Listener(on_press=self.on_pause, on_release=self.on_release, suppress=False)

        self.game = None

        self.field = None
        self.stop = False

        self.output = False
        self.no_flags = True
        self.auto_restart = True

    def on_click(self, x: int, y: int, button, pressed: bool):
        if self.field is None:
            self.field = GameField(x, y)

            self.listener.stop()

            print('Отлично, поле захвачено, старайся не двигать его и не перекрывать другими окнами. '
                  'Теперь просто переключись на окно с программой и нажми Enter чтобы начать игру')

            input()

            field = copy.deepcopy(self.field)
            while not self.stop:
                self.game = Game(field, self.output, self.no_flags)
                self.game.start_playing()

                if not self.auto_restart:
                    break

                field_copy = []
                for i in range(self.field.field_size_cubes_y):
                    field_copy.append([])
                    for j in range(self.field.field_size_cubes_x):
                        field_copy[-1].append(cell_type.Cell.CLOSED)

                field.field_array = field_copy

                pag.click(x=x, y=y, button="MIDDLE")
                time.sleep(1)
                pag.click(x=x, y=y, button="LEFT")

                field.update_field()

    def on_pause(self, key):
        if key == keyboard.Key.backspace:
            self.stop = True
            self.listener.stop()
            self.stop_listener.stop()

    def on_release(self, key):
        pass

    def main(self):

        print(
            'Привет, я ИИ, решающий игру Сапера. Я был написал BeBr0 для видео на ютуб. '
            'Так что если вдруг ты заметил какие-то ошибки, то пиши прямо ему. youtube.com/c/bebr0.\n\n'
            'Важно понимать, что работаю я только на сайте https://minesweeper.online/. '
            'Так что, прежде, чем продолжать, открой его. Еще одна важная вещь. '
            'В процессе работы программы, твой курсор будет заблокирован и будет полностью правляться программой, '
            'любое движение им с твоей стороны во время игры, может вызвать нежелательный результат игры или '
            'случайные клики в нежелаемые места '
            '(например в процессе написания я случайно выходил из системы пару раз :) )\n\n'
            ''
            'Поэтому, если хочешь прекратить работу скрипта, сначала нажми BACKSPACE '
            'и подожди остановки работы программы.\n\n'
            'Также, чтобы программа могла сама начинать новую игру, активируй в настройках сайта галочку '
            '"Начинать новую игру кликом средней кнопки мыши". \n\n'
            'Инструктаж закончен, приятного пользования (нажми Enter, что продолжить)'
        )

        input()

        print('Хотел бы, чтобы я выводил информацию о ходе игры в коноль? (да, нет)')

        while True:
            answer = input()
            if answer.lower() == 'да':
                self.output = True
                break
            elif answer.lower() == 'нет':
                self.output = False
                break
            else:
                print('Не понял. Введи "да" или "нет"')

        print('Понял. Хотел бы чтобы я проставлял флаги на месте мин на поле или нет? '
              '(Для победы это не обязательно) (да, нет)')

        while True:
            answer = input()
            if answer.lower() == 'да':
                self.no_flags = False
                break
            elif answer.lower() == 'нет':
                self.no_flags = True
                break
            else:
                print('Не понял. Введи "да" или "нет"')

        print('Понял. Включить безостановочную игру, с автоматическим началом новой игры или играть один раз? '
              '(да, нет)')

        while True:
            answer = input()
            if answer.lower() == 'да':
                self.auto_restart = True
                break
            elif answer.lower() == 'нет':
                self.auto_restart = False
                break
            else:
                print('Не понял. Введи "да" или "нет"')

        print(f'Спасибо! У нас получились такие настройки:\n\t'
              f'1. Вывод действий - {self.output}'
              f'\n\t2. Флаги на поле - {not self.no_flags}\n\t'
              f'3. Автоматическое начало новой игры - {self.auto_restart}\n\n'
              f' Нажми Enter, когда будешь готов начать игру.')

        input()

        print('Итак, чтобы начать нажми левой кнопкой мыши по любой клетке на поле. '
              'Не волнуйся, мины генерируются только после первого нажатия')

        self.listener.start()
        self.stop_listener.start()
        self.listener.join()


if __name__ == '__main__':
    Main().main()
