from cell_type import Cell
from game_detector import GameField


class Game:

    def __init__(self, game_field: GameField, output: bool, no_flags: bool):
        self.game_field = game_field

        self.is_stopped = False
        self.output = output
        self.no_flags = no_flags

    def start_playing(self):
        if self.output:
            print('\n=============================\n\nПогнали!')

        num = 1
        while num != 0:
            num = 0
            while self.__detect_to_flag():
                num += 1

            while self.__detect_to_open():
                num += 1

            if num == 0:
                if self.__get_safe_spot():
                    num += 1

            if self.is_stopped:

                if self.output:
                    print('Останавливаю игру')
                return

        win = True
        for row in self.game_field.field_array:
            for item in row:
                if item == Cell.CLOSED:
                    win = False

        if self.output:
            if win:
                print('ПОБЕДА!')
            else:
                print('Действия закончились')

    def __get_safe_spot(self) -> bool:
        chances = []
        for i in range(len(self.game_field.field_array)):
            chances.append([])
            for j in range(len(self.game_field.field_array[i])):
                chances[-1].append(0)

        for i in range(len(self.game_field.field_array)):
            for j in range(len(self.game_field.field_array[i])):
                if self.game_field.field_array[i][j] != Cell.CLOSED and self.game_field.field_array[i][j] != Cell.FLAG \
                        and self.game_field.field_array[i][j] != Cell.EMPTY:

                    mines = 0
                    closed = 0
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x != 0 or y != 0:
                                if len(self.game_field.field_array) > i + x >= 0 and len(
                                        self.game_field.field_array[i]) > j + y >= 0:

                                    if self.game_field.field_array[i + x][j + y] == Cell.FLAG:
                                        mines += 1
                                    elif self.game_field.field_array[i + x][j + y] == Cell.CLOSED:
                                        closed += 1

                    if closed != 0:
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if x != 0 or y != 0:
                                    if len(self.game_field.field_array) > i + x >= 0 and len(
                                            self.game_field.field_array[i]) > j + y >= 0:
                                        chances[i + x][j + y] += (self.game_field.field_array[i][
                                                                      j].num - mines) / closed

        current_min = 0
        min_x = -1
        min_y = -1

        for i in range(len(chances)):
            for j in range(len(chances[i])):
                if (chances[i][j] < current_min or current_min == 0) and chances[i][j] != 0 and \
                        self.game_field.field_array[i][j] == Cell.CLOSED:
                    current_min = chances[i][j]
                    min_x = i
                    min_y = j

        if min_x != -1:
            if self.output:
                print('Пытаюсь угадать...')
                print(f'Взял клетку с шансом встретить мину {chances[min_x][min_y]}, координаты {min_x} {min_y}')
            self.__open_ceil(min_x, min_y)
            if self.game_field.update_field():
                self.is_stopped = True
                if self.output:
                    print('Не угадал....')

            return True

        return False

    def __open_ceil(self, x: int, y: int):
        if self.game_field.field_array[x][y] == Cell.CLOSED:
            if self.output:
                print(f'Открываю клетку {x} {y}')
            self.game_field.put(x, y, Cell.EMPTY)

    def __put_flag(self, x: int, y: int):
        if self.game_field.field_array[x][y] != Cell.FLAG:
            if self.output:
                print(f'Нашел мину в {x} {y}')

            if not self.no_flags:
                self.game_field.put(x, y, Cell.FLAG)
            self.game_field.field_array[x][y] = Cell.FLAG

    def __detect_to_open(self) -> bool:
        action_done = False
        for ceil_type in Cell:
            if ceil_type != Cell.FLAG and ceil_type != Cell.CLOSED and ceil_type != Cell.EMPTY and ceil_type != Cell.BOMB:
                for i in range(len(self.game_field.field_array)):
                    for j in range(len(self.game_field.field_array[i])):
                        if self.game_field.field_array[i][j] == ceil_type:
                            mines_num = 0
                            for x in range(-1, 2):
                                for y in range(-1, 2):

                                    if len(self.game_field.field_array) > i + x >= 0 and \
                                            len(self.game_field.field_array[i]) > j + y >= 0:

                                        if self.game_field.field_array[i + x][j + y] == Cell.FLAG:
                                            mines_num += 1

                                            if mines_num > ceil_type.num:
                                                break

                            if mines_num == ceil_type.num:
                                for x in range(-1, 2):
                                    for y in range(-1, 2):
                                        if len(self.game_field.field_array) > i + x >= 0 and \
                                                len(self.game_field.field_array[i]) > j + y >= 0:

                                            if self.game_field.field_array[i + x][j + y] == Cell.CLOSED:
                                                self.__open_ceil(i + x, j + y)
                                                action_done = True

        if action_done:
            self.game_field.update_field()

        return action_done

    def __detect_to_flag(self) -> bool:
        action_done = False
        for ceil_type in Cell:
            if ceil_type != Cell.FLAG and ceil_type != Cell.CLOSED and ceil_type != Cell.EMPTY:
                for i in range(len(self.game_field.field_array)):
                    for j in range(len(self.game_field.field_array[i])):
                        if self.game_field.field_array[i][j] == ceil_type:

                            flags_num = 0
                            cords_x = []
                            cords_y = []
                            for x in range(-1, 2, 1):
                                for y in range(-1, 2, 1):
                                    if x != 0 or y != 0:
                                        if len(self.game_field.field_array) > i + x >= 0 and \
                                                len(self.game_field.field_array[i]) > j + y >= 0:

                                            if self.game_field.field_array[i + x][j + y] == Cell.CLOSED and \
                                                    self.game_field.field_array[i + x][j + y] != Cell.FLAG:

                                                cords_x.append(i + x)
                                                cords_y.append(j + y)

                                            elif self.game_field.field_array[i + x][j + y] == Cell.FLAG:
                                                flags_num += 1

                            if flags_num + len(cords_x) == ceil_type.num and len(cords_x) != 0:
                                action_done = True
                                for num in range(len(cords_x)):
                                    self.__put_flag(cords_x[num], cords_y[num])

        return action_done
