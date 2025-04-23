import streamlit as st
from game import render_game, init

st.set_page_config(
    page_title="Tic Tac Toe Bolt",
    page_icon="⚡",
    layout="centered",
)

if "board" not in st.session_state:
    st.session_state.opponent = 'AI'
    st.session_state.difficulty = 'Medium'
    init()

render_game()
