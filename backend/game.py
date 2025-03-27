import random
from typing import List
from ship_placement import place_classic_ships_id
from constants import SHIP_SIZES
from agent import RLAgent
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


BOARD_SIZE = 10

class Game:
    def __init__(self, game_id: str, ai_vs_ai: bool = False):
        self.game_id = game_id
        self.ai_vs_ai = ai_vs_ai

        self.board1 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board2 = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Массивы для ID кораблей
        self.board_id1 = [[-1]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board_id2 = [[-1]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Словари: ship_id -> количество оставшихся палуб
        self.ship_sizes1 = {}
        self.ship_sizes2 = {}

        # Расставляем
        place_classic_ships_id(self.board1, self.board_id1, self.ship_sizes1, SHIP_SIZES)
        place_classic_ships_id(self.board2, self.board_id2, self.ship_sizes2, SHIP_SIZES)

        self.current_player = 1
        self.ships1 = sum(SHIP_SIZES)  # 4 + 3+3 + 2+2+2 + 1+1+1+1 = 20
        self.ships2 = sum(SHIP_SIZES)

        self.game_over = False
        self.winner = None

        # Инициализация агента (пример)
        if ai_vs_ai:
            self.agent2 = RLAgent()
            self.agent2.start_new_game()
            logger.debug("agent2 создан для игрока 2.")
        else:
            logger.debug("ai_vs_ai = False, агент не создан для игрока 2.")

    # def place_random_ships(self, board: List[List[int]]):
    #     """Простейшее случайное размещение кораблей."""
    #     # Для упрощения ставим 20 одиночных палуб. 
    #     # В классическом морском бое логика сложнее (4-палубники, 3-палубники и т.д.).
    #     placed = 0
    #     while placed < 20:
    #         r = random.randint(0, BOARD_SIZE - 1)
    #         c = random.randint(0, BOARD_SIZE - 1)
    #         if board[r][c] == 0:
    #             board[r][c] = 1
    #             placed += 1


    def make_move(self, row: int, col: int):
        if self.game_over:
            return None

        if self.current_player == 1:
            target_board = self.board2
            target_board_id = self.board_id2
            ship_sizes = self.ship_sizes2
            opponent_ships = "ships2"
        else:
            target_board = self.board1
            target_board_id = self.board_id1
            ship_sizes = self.ship_sizes1
            opponent_ships = "ships1"

        cell = target_board[row][col]
        result = None

        if cell == 0:
            target_board[row][col] = 3  # промах
            result = "miss"
            self.switch_player()
        elif cell == 1:
            target_board[row][col] = 2  # попадание
            result = "hit"
            # Узнаем ID корабля
            ship_id = target_board_id[row][col]
            ship_sizes[ship_id] -= 1
            if ship_sizes[ship_id] <= 0:
                result = "sink"
            # Общий счётчик палуб
            setattr(self, opponent_ships, getattr(self, opponent_ships) - 1)
            if getattr(self, opponent_ships) <= 0:
                self.game_over = True
                self.winner = self.current_player
                # Можно оставить result="sink", либо "sink" + "game_over"
        else:
            # Уже было 2 (попадание) или 3 (промах)
            logger.debug(f"make_move: повторный выстрел в ({row},{col})")
        return result


    def ai_move(self):
        if self.game_over:
            logger.debug("Game is over. AI move not performed.")
            return None

        if self.current_player == 2 and hasattr(self, "agent2"):
            logger.debug("AI move: current_player is 2, calling agent2.get_next_shot().")
            shot = self.agent2.get_next_shot(self.board1)
            if shot is None:
                logger.debug("agent2.get_next_shot() returned None.")
                return None
            row, col = shot
            logger.debug(f"AI selected shot at ({row}, {col}).")
            result = self.make_move(row, col)
            logger.debug(f"Result of AI move: {result}.")
            # Передаем агенту поле board1, по которому он стреляет
            self.agent2.on_shot_result(row, col, result, self)
            return (row, col, result)
        else:
            logger.debug("ai_move() called but current_player is not 2 or agent2 is missing.")
            return None



    def switch_player(self):
        """Переключаем ход."""
        self.current_player = 2 if self.current_player == 1 else 1
        # Логирование нового игрока
        logger.debug(f"switch_player: новый current_player = {self.current_player}")
