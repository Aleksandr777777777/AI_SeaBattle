# backend/game.py

import random
from typing import List
from ship_placement import place_classic_ships

BOARD_SIZE = 10

class Game:
    def __init__(self, game_id: str, ai_vs_ai: bool = True):
        self.game_id = game_id
        self.ai_vs_ai = ai_vs_ai
        
        # Два поля (списки списков), по 10х10
        # 0 = пусто, 1 = корабль, 2 = попадание, 3 = промах
        # self.board1 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        # self.board2 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        """
        Расстановка кораблей как в классической игре
        """
        
        self.board1 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board2 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        place_classic_ships(self.board1)
        place_classic_ships(self.board2)
        
        # Расставим корабли случайно для обоих
        # self.place_random_ships(self.board1)
        # self.place_random_ships(self.board2)
        
        # Укажем, что первый ходит Player1 (можно рандом)
        self.current_player = 1
        
        # Количество «живых» палуб (упростим, чтобы понять, когда игра закончилась)
        self.ships1 = 20  # например, 20 палуб на все корабли
        self.ships2 = 20
        
        # Флаг окончания игры
        self.game_over = False
        self.winner = None

    def place_random_ships(self, board: List[List[int]]):
        """Простейшее случайное размещение кораблей."""
        # Для упрощения ставим 20 одиночных палуб. 
        # В классическом морском бое логика сложнее (4-палубники, 3-палубники и т.д.).
        placed = 0
        while placed < 20:
            r = random.randint(0, BOARD_SIZE - 1)
            c = random.randint(0, BOARD_SIZE - 1)
            if board[r][c] == 0:
                board[r][c] = 1
                placed += 1

    def make_move(self, row: int, col: int):
        """Обработка выстрела по клетке (row, col)."""
        if self.game_over:
            return
        
        if self.current_player == 1:
            target_board = self.board2
            opponent_ships = "ships2"
        else:
            target_board = self.board1
            opponent_ships = "ships1"

        cell = target_board[row][col]
        if cell == 0:
            # Промах
            target_board[row][col] = 3
            self.switch_player()
        elif cell == 1:
            # Попадание
            target_board[row][col] = 2
            setattr(self, opponent_ships, getattr(self, opponent_ships) - 1)
            # Проверим, не закончилась ли игра
            if getattr(self, opponent_ships) <= 0:
                self.game_over = True
                self.winner = self.current_player
            else:
                # При попадании тот же игрок ходит снова (правило можно менять)
                pass
        # Если клетка уже 2 или 3, значит повторный выстрел, можно проигнорировать 
        # или тоже переключить ход - это на твое усмотрение.

    def switch_player(self):
        """Переключаем ход."""
        self.current_player = 2 if self.current_player == 1 else 1
