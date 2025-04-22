import streamlit as st
from game import render_game, init

if "board" not in st.session_state:
    st.session_state.opponent = 'Human'
    st.session_state.prev_opponent = 'Human'
    st.session_state.difficulty = 'Easy'
    init()

render_game()
