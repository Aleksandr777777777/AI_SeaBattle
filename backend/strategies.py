"""
Описание: 4 стратегии стрельбы для поля 10x10.
"""

def pattern_image_1():
    """
    Пример: «шахматный» паттерн, сначала клетки (r+c)%2==0, потом (r+c)%2==1.
    """
    coords = []
    # Сначала проходим клетки, где (r+c) чётное
    for r in range(10):
        for c in range(10):
            if (r + c) % 2 == 0:
                coords.append((r, c))
    # Затем клетки, где (r+c) нечётное
    for r in range(10):
        for c in range(10):
            if (r + c) % 2 == 1:
                coords.append((r, c))
    return coords

def pattern_image_2():
    """
    Пример: «шахматный» паттерн, но в обратном порядке —
    сначала (r+c) % 2 == 1, потом (r+c) % 2 == 0.
    """
    coords = []
    # Сначала проходим клетки, где (r+c) нечётное
    for r in range(10):
        for c in range(10):
            if (r + c) % 2 == 1:
                coords.append((r, c))
    # Затем клетки, где (r+c) чётное
    for r in range(10):
        for c in range(10):
            if (r + c) % 2 == 0:
                coords.append((r, c))
    return coords

def quadrant_pattern():
    """
    Разделяем поле на «блоки» 3×3. Сначала идём по блоку (0,0)-(2,2), затем (0,3)-(2,5) и т.д.
    Учтём, что 10 не делится на 3, поэтому последние строки/столбцы будут меньше 3.
    """
    coords = []
    block_size = 3
    for block_row in range(0, 10, block_size):
        for block_col in range(0, 10, block_size):
            # Добавляем клетки внутри блока
            for r in range(block_row, min(block_row + block_size, 10)):
                for c in range(block_col, min(block_col + block_size, 10)):
                    coords.append((r, c))
    return coords

def spiral_pattern():
    """
    Обходим поле 10x10 по спирали из левого верхнего угла (0,0), идём вправо,
    упираемся в границу или уже посещённую клетку, поворачиваем вниз, и т.д.
    """
    coords = []
    n = 10
    visited = [[False]*n for _ in range(n)]
    # Направления: вправо, вниз, влево, вверх
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    d_idx = 0  # индекс текущего направления
    r, c = 0, 0

    for _ in range(n*n):
        coords.append((r, c))
        visited[r][c] = True
        # Пробуем идти вперёд
        nr = r + directions[d_idx][0]
        nc = c + directions[d_idx][1]

        # Если вышли за границы или наткнулись на посещённую клетку — поворот
        if not (0 <= nr < n and 0 <= nc < n and not visited[nr][nc]):
            d_idx = (d_idx + 1) % 4
            nr = r + directions[d_idx][0]
            nc = c + directions[d_idx][1]

        r, c = nr, nc

    return coords

PATTERN_IMAGE_1 = pattern_image_1()
PATTERN_IMAGE_2 = pattern_image_2()
PATTERN_QUADRANT = quadrant_pattern()
PATTERN_SPIRAL = spiral_pattern()

ALL_PATTERNS = [
    PATTERN_IMAGE_1,
    PATTERN_IMAGE_2,
    PATTERN_QUADRANT,
    PATTERN_SPIRAL,
]

