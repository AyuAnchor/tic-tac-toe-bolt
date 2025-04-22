import numpy as np
import streamlit as st
import random
from ai import minimax
from constants import SYMBOLS, DIFFICULTY_DEPTH
from helpers import check_available_moves, check_game_over

def init(post_init=False):
    if not post_init:
        st.session_state.win = {'X': 0, 'O': 0}
    st.session_state.board = np.full((3, 3), '.', dtype=str)
    st.session_state.player = 'X'
    st.session_state.warning = False
    st.session_state.winner = None
    st.session_state.over = False
    st.session_state.move_history = {'X': [], 'O': []}

def make_move(i, j, player):
    board = st.session_state.board
    board[i][j] = player
    st.session_state.move_history[player].append((i, j))
    if len(st.session_state.move_history[player]) > 3:
        old_i, old_j = st.session_state.move_history[player].pop(0)
        board[old_i][old_j] = '.'

def ai_move():
    level = st.session_state.difficulty
    max_depth = DIFFICULTY_DEPTH[level]
    if max_depth == 0:
        move = random.choice(check_available_moves(extra=True))
    else:
        _, move = minimax(st.session_state.board.copy(),
                          {k: v[:] for k, v in st.session_state.move_history.items()},
                          0, True, max_depth)
    if move:
        make_move(*move, 'O')
        check_game_over()

def handle_click(i, j):
    if st.session_state.over or (i, j) not in check_available_moves(extra=True):
        return
    make_move(i, j, st.session_state.player)
    check_game_over()
    if not st.session_state.over and st.session_state.opponent == 'AI' and st.session_state.player == 'O':
        ai_move()

def render_game():
    st.title("⚡ Tic Tac Toe Bolt", help="⚡️ Bolt Rule: After a player places 3 marks, their oldest mark disappears")

    # Opponent and Difficulty in sidebar for mobile responsiveness
    opponent_column, difficulty_column = st.columns([1, 1])

    with opponent_column:
        current_opponent = st.selectbox("Set Opponent", ['Human', 'AI'], key="opponent")
    with difficulty_column:
        current_difficulty = st.selectbox("AI Difficulty", ['Easy', 'Medium', 'Hard'], key="difficulty") if current_opponent == 'AI' else None

    # Reset on opponent change
    if 'prev_opponent' not in st.session_state:
        st.session_state.prev_opponent = current_opponent
    elif st.session_state.prev_opponent != current_opponent:
        st.session_state.prev_opponent = current_opponent
        init(post_init=False)

    # Win message
    if st.session_state.winner:
        st.success(f"🎉 {SYMBOLS[st.session_state.winner]} wins!")

    st.markdown("### ")
    for i, row in enumerate(st.session_state.board):
        cols = st.columns([5, 1, 1, 1, 5])
        for j, val in enumerate(row):
            symbol = SYMBOLS[val]
            cols[j + 1].button(
                symbol,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
                use_container_width=True
            )

    # Game controls (win counter, current player, restart button)
    st.markdown("### ")
    control_row = st.columns([1, 1, 1, 1, 1, 2])
    with control_row[1]:
        st.write(f"{SYMBOLS[st.session_state.player]}'s Turn")
    with control_row[3]:
        st.write(f"❎ {st.session_state.win['X']} - {st.session_state.win['O']} 🅾️")
    with control_row[5]:
        st.button("🔄 Restart", on_click=init, args=(True,))
