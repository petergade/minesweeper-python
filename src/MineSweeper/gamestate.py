from typing import List
from common import SpecialSquareValues, GameResultType
import random
import time

FOG = SpecialSquareValues.FOG
MINE = SpecialSquareValues.MINE
FLAG = SpecialSquareValues.FLAG


class GameState:

    def __init__(self, width: int, height: int, mines: int):
        self.mines: int = mines
        self.width: int = width
        self.height: int = height
        self.player_map: List[List[int]] = [[FOG for _ in range(width)] for _ in range(height)]
        self.game_map: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        self.is_initialized = False
        self.game_result_type: GameResultType = GameResultType.UNKNOWN
        self.game_duration_in_seconds = None
        self.game_started = None
        self.game_finished = None
        self.mines_not_selected = mines

    def initialize_game_map(self, row_selected, column_selected):
        self.game_started = time.time()
        mines_count = 0
        while mines_count < self.mines:
            row = random.randint(0, self.height - 1)
            column = random.randint(0, self.width - 1)

            if (abs(row - row_selected) > 1 or abs(column - column_selected) > 1) and \
                    self.game_map[row][column] != MINE:
                self.game_map[row][column] = MINE
                mines_count += 1
                directions = ((-1, -1), (-1, 0), (-1, 1), (1, 0), (1, 1), (1, -1), (0, -1), (0, 1))
                for direction in directions:
                    end_row = row + direction[0]
                    end_col = column + direction[1]
                    if 0 <= end_row < self.height and 0 <= end_col < self.width:
                        if self.game_map[end_row][end_col] != MINE:
                            self.game_map[end_row][end_col] += 1

        self.is_initialized = True

    def reveal(self, row, column):
        if not self.is_initialized:
            # prvni klik, inicializujeme hru
            self.initialize_game_map(row, column)
        if self.player_map[row][column] == FLAG:
            return False
        elif self.game_map[row][column] == MINE:
            self.end_game(GameResultType.LOST)
            return True
        else:
            self.player_map[row][column] = self.game_map[row][column]
            if self.check_victory():
                return False
            print(f"row: {row}, column: {column}, value: {self.player_map[row][column]}")
            if self.player_map[row][column] == 0:
                directions = ((-1, -1), (-1, 0), (-1, 1), (1, 0), (1, 1), (1, -1), (0, -1), (0, 1))
                for direction in directions:
                    end_row: int = row + direction[0]
                    end_col: int = column + direction[1]
                    if 0 <= end_row < self.height and 0 <= end_col < self.width:
                        if self.player_map[end_row][end_col] == FOG:
                            self.reveal(end_row, end_col)
                return False
            else:
                return False

    def end_game(self, result_type):
        self.game_result_type = result_type
        self.game_finished = time.time()
        self.game_duration_in_seconds = self.game_finished - self.game_started
        print(f'Result: {str(result_type)}, Elapsed seconds: {self.game_duration_in_seconds}')

    def add_flag(self, row, column):
        if self.player_map[row][column] == FOG:
            self.player_map[row][column] = FLAG
            self.mines_not_selected -= 1
        elif self.player_map[row][column] == FLAG:
            self.player_map[row][column] = FOG
            self.mines_not_selected += 1

    def check_victory(self) -> bool:
        unrevealed_count = self.get_unrevealed_count()
        print(f'Unrevealed_count count: {unrevealed_count}')
        if unrevealed_count == self.mines:
            self.end_game(GameResultType.WIN)
            return True
        return False

    def get_unrevealed_count(self):
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.player_map[i][j] == SpecialSquareValues.FOG or self.player_map[i][j] == SpecialSquareValues.FLAG:
                    count += 1
        return count

    def get_elapsed_time(self):
        if self.is_initialized:
            return time.time() - self.game_started
        else:
            return None

