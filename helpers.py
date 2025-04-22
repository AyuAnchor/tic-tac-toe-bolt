import streamlit as st

def check_available_moves(board=None, extra=False):
    if board is None:
        board = st.session_state.board
    raw = board.flatten().tolist()
    moves = [i for i, cell in enumerate(raw) if cell == '.']
    return [(i // 3, i % 3) for i in moves] if extra else moves

def check_rows(board):
    for row in board:
        if len(set(row)) == 1 and row[0] != '.':
            return row[0]
    return None

def check_diagonals(board):
    if len(set([board[i][i] for i in range(3)])) == 1 and board[0][0] != '.':
        return board[0][0]
    if len(set([board[i][2 - i] for i in range(3)])) == 1 and board[0][2] != '.':
        return board[0][2]
    return None

def check_win(board):
    for b in [board, board.T]:
        winner = check_rows(b)
        if winner:
            return winner
    return check_diagonals(board)

def check_game_over():
    winner = check_win(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.win[winner] += 1
        st.session_state.over = True
    elif not check_available_moves():
        st.session_state.over = True
    else:
        st.session_state.player = 'O' if st.session_state.player == 'X' else 'X'
