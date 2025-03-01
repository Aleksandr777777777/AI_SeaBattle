from constants import SHIP_SIZES
import random

def can_place_ship(board, row, col, size, horizontal):
    """
    Проверяем можно ли поставить корабль длины size
    начиная с клетки (row, col), горизонтально или вертикально,
    без выхода за границы касаний.
    """
    board_size = 10
    
    """
    Проверка выхода за границы поля 
    """
    if horizontal:
        if col + size > board_size:
            return False
    else:
        if row + size > board_size:
            return False
        
    """
    Проходим по всем клеткам, где будет корабль, и вокруг них
    чтобы убедится, что нет пересечений и касаний 
    """
    
    for i in range(size):
        r = row + (i if not horizontal else 0)
        c = col + (i if horizontal else 0)
        
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if 0 <= nr < board_size and 0 <= nc < board_size:
                    if board[nr][nc] != 0:
                        return False
    return True

def place_ship(board, row, col, size, horizontal):
    """
    Установка корабля (значение 1) на доску
    """
    
    for i in range(size):
        r = row + (i if not horizontal else 0)
        c = col + (i if horizontal else 0)
        board[r][c] = 1
        
def place_classic_ships(board):
    """
    Расставляем корабли по классическим правилам:
    1х4, 2х3, 3х2, 4х1, без касаний
    """
    
    for size in SHIP_SIZES:
        placed = False
        attempts = 0
        while not placed:
            attempts += 1
            if attempts > 1000:
                raise Exception(f"Не удалось разместить корабль размера {size} после 1000 попыток")

            horizontal = (random.randint(0, 1) == 0)
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            
            if can_place_ship(board, row, col, size, horizontal):
                place_ship(board, row, col, size, horizontal)
                placed = True
