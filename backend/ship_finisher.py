def update_finishing_targets(current_hits, to_finish, result, row, col, board):
    """
    Обновляет списки current_hits и to_finish на основе результата выстрела.
    """
    print(f"[DEBUG] Shot at ({row},{col}) result: {result}")
    
    if result == "hit":
        # Добавляем текущее попадание, если его ещё нет
        if (row, col) not in current_hits:
            current_hits.append((row, col))
        
        # Если это первое попадание, добавляем всех соседей
        if len(current_hits) == 1:
            neighbors = get_adjacent_cells(row, col, board)
            for n in neighbors:
                if n not in to_finish:
                    to_finish.append(n)
        elif len(current_hits) >= 2:
            # Определяем направление (горизонтальное или вертикальное) по первым двум попаданиям
            first_hit = current_hits[0]
            second_hit = current_hits[1]
            # Если горизонтальное направление
            if first_hit[0] == second_hit[0]:
                row_fixed = first_hit[0]
                cols = [hit[1] for hit in current_hits]
                min_c, max_c = min(cols), max(cols)
                # Кандидаты – слева от min и справа от max
                left_candidate = (row_fixed, min_c - 1)
                right_candidate = (row_fixed, max_c + 1)
                # Обновляем список: вместо полного очищения, удалим невалидные и добавим новые
                to_finish = [cell for cell in to_finish if is_valid_target(cell, board)]
                for candidate in [left_candidate, right_candidate]:
                    if is_valid_target(candidate, board) and candidate not in to_finish:
                        to_finish.append(candidate)
            elif first_hit[1] == second_hit[1]:
                # Вертикальное направление
                col_fixed = first_hit[1]
                rows = [hit[0] for hit in current_hits]
                min_r, max_r = min(rows), max(rows)
                up_candidate = (min_r - 1, col_fixed)
                down_candidate = (max_r + 1, col_fixed)
                to_finish = [cell for cell in to_finish if is_valid_target(cell, board)]
                for candidate in [up_candidate, down_candidate]:
                    if is_valid_target(candidate, board) and candidate not in to_finish:
                        to_finish.append(candidate)
            else:
                # Если попадания не выстроены строго горизонтально или вертикально,
                # добавляем соседей для последнего попадания
                neighbors = get_adjacent_cells(row, col, board)
                for n in neighbors:
                    if is_valid_target(n, board) and n not in to_finish:
                        to_finish.append(n)
    elif result == "sink":
        print(f"[DEBUG] Ship sunk at ({row},{col}). Clearing targets.")
        current_hits.clear()
        to_finish.clear()

    print(f"[DEBUG] To finish list: {to_finish}")
    return current_hits, to_finish



def get_adjacent_cells(row, col, board):
    """
    Возвращает список соседних клеток (4 направления) для координаты (row, col),
    где значение board[r][c] равно 0 или 1.
    """
    candidates = []
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 10 and 0 <= nc < 10:
            if board[nr][nc] in [0, 1]:
                candidates.append((nr, nc))
    return candidates


def is_valid_target(cell, board):
    r, c = cell
    return 0 <= r < 10 and 0 <= c < 10 and board[r][c] in [0, 1]

