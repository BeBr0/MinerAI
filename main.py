import game_detector
from pynput import mouse


def on_click(x: int, y: int, button, pressed: bool):
    print(1)
    game_detector.detect_field(x, y)

    lst = [x for x in range(10) if x % 2 == 0]


def main():
    print('Привет, я ИИ, решающий игру Сапера. Чтобы начать напиши start: ')
    inp = input()

    if inp == 'start':
        print('Теперь нажми на любую клетку сапера. Не волнуйся, мины генерируются после первого нажатия :) (только в '
              'игре)')

        with mouse.Listener(on_click=on_click, suppress=False) as listener:
            listener.join()


if __name__ == '__main__':
    main()
