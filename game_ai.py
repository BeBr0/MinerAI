from cell_type import Cell
from game_detector import GameField


class Game:

    def __init__(self, game_field: GameField):
        self.game_field = game_field
        self.is_stopped = False

        self.__start_playing()

    def __start_playing(self):
        num = 1
        while num != 0:
            num = 0
            while self.__detect_to_flag():
                num += 1

                if self.is_stopped:
                    return

            while self.__detect_to_open():
                num += 1

                if self.is_stopped:
                    return

    def __open_ceil(self, x: int, y: int):
        self.game_field.put(x, y, Cell.EMPTY)

        self.game_field.update_field()

    def __put_flag(self, x: int, y: int):
        if self.game_field.field_array[x][y] != Cell.FLAG:
            self.game_field.field_array[x][y] = Cell.FLAG
            self.game_field.put(x, y, Cell.FLAG)

    def __detect_to_open(self) -> bool:
        action_done = False
        for ceil_type in Cell:
            if ceil_type != Cell.FLAG and ceil_type != Cell.CLOSED and ceil_type != Cell.EMPTY:
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

                                            if mines_num > 1:
                                                break

                            if mines_num == ceil_type.num:
                                for x in range(-1, 2):
                                    for y in range(-1, 2):
                                        if self.game_field.field_array[i + x][j + y] == Cell.CLOSED:
                                            self.__open_ceil(i + x, j + y)
                                            action_done = True

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
                            for x in range(-1, 2):
                                for y in range(-1, 2):
                                    if x != 0 or y != 0:
                                        if len(self.game_field.field_array) > i + x >= 0 and \
                                                len(self.game_field.field_array[i]) > j + y >= 0:

                                            if self.game_field.field_array[i + x][j + y] == Cell.CLOSED and \
                                                    self.game_field.field_array[i + x][j + y] != Cell.FLAG:

                                                cords_x.append(i + x)
                                                cords_y.append(j + y)

                                            elif self.game_field.field_array[i + x][j + y] == Cell.FLAG:
                                                flags_num += 1

                            print(flags_num, len(cords_x), ceil_type)
                            if flags_num + len(cords_x) == ceil_type.num:
                                action_done = True
                                for num in range(len(cords_x)):
                                    self.__put_flag(cords_x[num], cords_y[num])

        return action_done
