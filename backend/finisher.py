from typing import List, Tuple, Set

class ShipFinisher:
    def __init__(self):
        self.hits: List[Tuple[int, int]] = []
        self.direction: str = None
        self.cells_to_shoot: List[Tuple[int, int]] = []
        self.all_shot_cells: Set[Tuple[int, int]] = set()  # Все выстрелы (попадания + промахи)
        self.misses: Set[Tuple[int, int]] = set()  # Только промахи

    def reset(self):
        self.hits = []
        self.direction = None
        self.cells_to_shoot = []
        print("[Finisher] RESET: Корабль потоплен.")

    def add_shot_result(self, row: int, col: int, result: str, board_size: int = 10):
        """Обновляет данные на основе результата выстрела."""
        self.all_shot_cells.add((row, col))

        if result == "hit":
            if (row, col) in self.hits:
                print(f"[Finisher] WARNING: Повторное попадание в ({row}, {col}).")
                return

            self.hits.append((row, col))
            print(f"[Finisher] Попадание в ({row}, {col}). Текущие попадания: {self.hits}")
            self._update_direction()
            self._update_cells_to_shoot(board_size)

        elif result == "miss":
            self.misses.add((row, col))
            print(f"[Finisher] Промах в ({row}, {col}).")
            
    def _update_direction(self):
        if len(self.hits) >= 2 and not self.direction:
            r1, c1 = self.hits[0]
            r2, c2 = self.hits[1]
            self.direction = 'horizontal' if r1 == r2 else 'vertical'
            print(f"[Finisher] Направление корабля: {self.direction}")

    def _update_cells_to_shoot(self, board_size: int):
        new_cells = []
        
        if not self.direction:
            # Режим поиска: стреляем в соседей подбитых палуб, исключая промахи
            for (r, c) in self.hits:
                neighbors = self._get_adjacent_cells(r, c, board_size)
                new_cells.extend([(nr, nc) for (nr, nc) in neighbors 
                                if (nr, nc) not in self.all_shot_cells])
        else:
            # Режим добивания: стреляем только вдоль оси
            if self.direction == "horizontal":
                min_col = min(c for (_, c) in self.hits)
                max_col = max(c for (_, c) in self.hits)
                r = self.hits[0][0]
                candidates = [(r, min_col - 1), (r, max_col + 1)]
            else:  # vertical
                min_row = min(r for (r, _) in self.hits)
                max_row = max(r for (r, _) in self.hits)
                c = self.hits[0][1]
                candidates = [(min_row - 1, c), (max_row + 1, c)]

            new_cells.extend([(r, c) for (r, c) in candidates 
                            if (0 <= r < board_size) and (0 <= c < board_size)
                            and (r, c) not in self.all_shot_cells])

        self.cells_to_shoot = list(set(new_cells))  # Удаляем дубликаты
        print(f"[Finisher] Новые клетки для выстрела: {self.cells_to_shoot}")

    def get_next_shot(self) -> Tuple[int, int] | None:
        if not self.cells_to_shoot:
            print("[Finisher] Нет клеток для добивания.")
            return None

        next_shot = self.cells_to_shoot.pop(0)
        print(f"[Finisher] Выстрел в {next_shot}")
        return next_shot

    def _get_adjacent_cells(self, row: int, col: int, board_size: int) -> List[Tuple[int, int]]:
        """Возвращает 4 соседние клетки (без диагоналей)."""
        cells = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < board_size and 0 <= nc < board_size:
                cells.append((nr, nc))
        return cells