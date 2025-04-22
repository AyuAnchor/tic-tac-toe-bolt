from helpers import check_available_moves, check_win

def minimax(board, move_histories, depth, is_maximizing, max_depth):
    winner = check_win(board)
    if winner == 'O':
        return 10 - depth, None
    elif winner == 'X':
        return depth - 10, None
    elif not check_available_moves(board) or depth >= max_depth:
        return 0, None

    player = 'O' if is_maximizing else 'X'
    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = None

    for i, j in check_available_moves(board, extra=True):
        board[i][j] = player
        move_histories[player].append((i, j))
        removed = None
        if len(move_histories[player]) > 3:
            removed = move_histories[player].pop(0)
            board[removed[0]][removed[1]] = '.'

        score, _ = minimax(board.copy(), {
            'X': move_histories['X'][:],
            'O': move_histories['O'][:]
        }, depth + 1, not is_maximizing, max_depth)

        board[i][j] = '.'
        move_histories[player].pop()
        if removed:
            move_histories[player].insert(0, removed)
            board[removed[0]][removed[1]] = player

        if is_maximizing and score > best_score:
            best_score = score
            best_move = (i, j)
        elif not is_maximizing and score < best_score:
            best_score = score
            best_move = (i, j)

    return best_score, best_move
