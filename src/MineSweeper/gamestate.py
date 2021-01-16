from typing import List, Tuple
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
        self.elapsed_seconds = None
        self.game_started = None
        self.game_finished = None

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
        if self.game_map[row][column] == MINE:
            self.game_result_type = GameResultType.LOST
            self.game_finished = time.time()
            self.elapsed_seconds = self.game_finished - self.game_started
            print(f'Elapsed seconds: {self.elapsed_seconds}')
        else:
            self.player_map[row][column] = self.game_map[row][column]
            print(f"row: {row}, column: {column}, value: {self.player_map[row][column]}")
            if self.player_map[row][column] == 0:
                directions = ((-1, -1), (-1, 0), (-1, 1), (1, 0), (1, 1), (1, -1), (0, -1), (0, 1))
                for direction in directions:
                    end_row: int = row + direction[0]
                    end_col: int = column + direction[1]
                    if end_row < 0 or end_row >= self.height or end_col < 0 or end_col >= self.width:
                        # jsme mimo hraci pole
                        next
                    else:
                        if self.player_map[end_row][end_col] == FOG:
                            self.reveal(end_row, end_col)
            else:
                return

    def add_flag(self, row, column):
        if self.player_map[row][column] == FOG:
            self.player_map[row][column] = FLAG
        elif self.player_map[row][column] == FLAG:
            self.player_map[row][column] = FOG
