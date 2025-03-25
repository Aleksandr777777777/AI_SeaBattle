import random

def can_place_ship_id(board, row, col, size, horizontal):
    """
    Проверяем можно ли поставить корабль длины size
    начиная с клетки (row, col), горизонтально или вертикально,
    без выхода за границы и без касаний.
    (Логика та же, что и в can_place_ship)
    """
    board_size = 10

    if horizontal:
        if col + size > board_size:
            return False
    else:
        if row + size > board_size:
            return False

    for i in range(size):
        r = row + (i if not horizontal else 0)
        c = col + (i if horizontal else 0)
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if 0 <= nr < board_size and 0 <= nc < board_size:
                    if board[nr][nc] != 0:
                        return False
    return True

def place_ship_id(board, board_id, row, col, size, horizontal, ship_id):
    """
    Установка корабля (значение 1) на доску.
    Параллельно заполняем board_id[r][c] = ship_id.
    """
    for i in range(size):
        r = row + (i if not horizontal else 0)
        c = col + (i if horizontal else 0)
        board[r][c] = 1
        board_id[r][c] = ship_id

def place_classic_ships_id(board, board_id, ship_sizes, ship_sizes_list):
    """
    Расставляем корабли по классическим правилам:
    ship_sizes_list, например [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    Параллельно заполняем board_id и ship_sizes (dict).
    Возвращаем (board, board_id, ship_sizes).
    """
    board_size = 10
    ship_id_counter = 0

    for size in ship_sizes_list:
        placed = False
        attempts = 0
        while not placed:
            attempts += 1
            if attempts > 1000:
                raise Exception(f"Не удалось разместить корабль размера {size} после 1000 попыток")

            horizontal = (random.randint(0, 1) == 0)
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - 1)

            if can_place_ship_id(board, row, col, size, horizontal):
                place_ship_id(board, board_id, row, col, size, horizontal, ship_id_counter)
                ship_sizes[ship_id_counter] = size  # сохранили размер корабля
                ship_id_counter += 1
                placed = True

    return board, board_id, ship_sizes
