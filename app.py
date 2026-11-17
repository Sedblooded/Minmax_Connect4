import random
import streamlit as st

from engine import (
    COLS, ROWS, COMPUTER, PLAYER,
    create_board, drop_coin, get_valid_locations,
    get_ai_move, check_winner,
)

st.set_page_config(
    page_title="Connect 4 AI",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root { color-scheme: dark; }
.stApp {
    background: #171615;
    color: #f1efed;
    font-family: Inter, sans-serif;
}
header[data-testid="stHeader"] { background: #171615; }
.block-container {
    max-width: 980px;
    padding-top: 1.35rem;
    padding-bottom: 2.5rem;
}
h1 {
    text-align: center;
    font-size: clamp(2.2rem, 5vw, 3.35rem) !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px;
    margin: 0 0 1.15rem 0 !important;
}
div[data-testid="stExpander"] {
    border: 1px solid #484542;
    border-radius: 12px;
    background: transparent;
    margin-bottom: 1rem;
}
div[data-testid="stExpander"] summary {
    font-weight: 600;
}
.stButton > button {
    min-height: 52px;
    border: 1px solid #484542;
    border-radius: 12px;
    background: #201f1d;
    color: #eeeae7;
    font-weight: 600;
    transition: border-color .15s, background .15s;
}
.stButton > button:hover {
    border-color: #e34b78;
    color: white;
    background: #292522;
}
.stButton > button:disabled {
    opacity: .38;
}
div[data-testid="stHorizontalBlock"] { gap: 12px; }
div[data-testid="stMetric"] {
    background: #201f1d;
    border: 1px solid #403d39;
    border-radius: 10px;
    padding: 12px;
}
.game-status {
    text-align: center;
    color: #e8e3df;
    font-size: 1rem;
    font-weight: 600;
    padding: 12px 0 15px;
}
.board-shell {
    width: 100%;
    margin: 22px auto 10px;
}
.board-grid {
    display: grid;
    grid-template-columns: repeat(8, minmax(0, 1fr));
    column-gap: clamp(9px, 2.7vw, 29px);
    row-gap: clamp(14px, 2.6vw, 28px);
    padding: 0 2.3%;
}
.hole {
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    background: radial-gradient(circle at 36% 28%, #ffffff 0%, #eee8f4 37%, #d9c6e7 72%, #b99bcf 100%);
    box-shadow: inset 0 1px 3px rgba(255,255,255,.7), 0 1px 2px rgba(0,0,0,.28);
}
.hole.player {
    background: radial-gradient(circle at 34% 27%, #ff8295 0%, #f04465 48%, #c91e48 100%);
    box-shadow: inset 0 1px 3px rgba(255,255,255,.45), 0 2px 4px rgba(0,0,0,.3);
}
.hole.ai {
    background: radial-gradient(circle at 34% 27%, #ffe88b 0%, #f6c94e 48%, #d99a24 100%);
    box-shadow: inset 0 1px 3px rgba(255,255,255,.5), 0 2px 4px rgba(0,0,0,.3);
}
.arrow-row { margin-top: 1.1rem; }
.arrow-row .stButton > button {
    min-height: 53px;
    color: #e83f75;
    font-size: 1.15rem;
}
.small-note {
    text-align: center;
    color: #928b85;
    font-size: .82rem;
    margin-top: 12px;
}
@media (max-width: 650px) {
    .block-container { padding-left: .7rem; padding-right: .7rem; }
    .board-grid { column-gap: 7px; row-gap: 10px; padding: 0 1%; }
    .stButton > button { min-height: 43px; padding: 0 .2rem; }
}
</style>
""", unsafe_allow_html=True)


def new_game(human_starts: bool):
    st.session_state.board = create_board()
    st.session_state.turn = PLAYER if human_starts else COMPUTER
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.moves = 0
    st.session_state.last_column = None


if "board" not in st.session_state:
    new_game(True)
    st.session_state.depth = 4


def finish_if_needed():
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    elif not get_valid_locations(st.session_state.board):
        st.session_state.winner = "DRAW"
        st.session_state.game_over = True


def play_move(column, coin):
    if st.session_state.game_over:
        return
    if column not in get_valid_locations(st.session_state.board):
        return
    if drop_coin(st.session_state.board, coin, column):
        st.session_state.moves += 1
        st.session_state.last_column = column
        finish_if_needed()


def render_board():
    # Render top-to-bottom while engine storage remains bottom-to-top.
    html = ['<div class="board-shell"><div class="board-grid">']
    for row in range(ROWS - 1, -1, -1):
        for col in range(COLS):
            value = st.session_state.board[col][row]
            css = "hole"
            if value == PLAYER:
                css += " player"
            elif value == COMPUTER:
                css += " ai"
            html.append(f'<div class="{css}"></div>')
    html.append("</div></div>")
    st.markdown("".join(html), unsafe_allow_html=True)


st.title("Connect 4 AI")

with st.expander("CONNECT 4", expanded=False):
    st.markdown(
        "**How to play**  \n"
        "Drop a coin into a column. The first player to connect four "
        "horizontally, vertically, or diagonally wins.  \n\n"
        "**Players:** You are pink/red (X); the AI is yellow (O)."
    )
    st.slider(
        "AI search depth",
        min_value=1,
        max_value=8,
        value=st.session_state.depth,
        key="depth",
        help="Higher values search further ahead and can take longer.",
    )
    st.caption("AI: Minimax with Alpha-Beta pruning and the supplied window scoring.")

start_left, start_right = st.columns(2)
with start_left:
    if st.button("New Game (You Start)", use_container_width=True):
        new_game(True)
        st.rerun()
with start_right:
    if st.button("New Game (AI Starts)", use_container_width=True):
        new_game(False)
        st.rerun()

if st.session_state.game_over:
    if st.session_state.winner == PLAYER:
        message = "🎉 You win!"
    elif st.session_state.winner == COMPUTER:
        message = "🤖 AI wins!"
    else:
        message = "🤝 Draw game!"
elif st.session_state.turn == PLAYER:
    message = "Your turn — choose a column"
else:
    message = "AI is thinking..."

st.markdown(f'<div class="game-status">{message}</div>', unsafe_allow_html=True)

# Column drop controls, visually aligned above the board.
arrow_cols = st.columns(COLS)
for col, container in enumerate(arrow_cols):
    with container:
        disabled = (
            st.session_state.game_over
            or st.session_state.turn != PLAYER
            or col not in get_valid_locations(st.session_state.board)
        )
        if st.button("▾", key=f"drop_{col}", disabled=disabled, use_container_width=True):
            play_move(col, PLAYER)
            if not st.session_state.game_over:
                st.session_state.turn = COMPUTER
            st.rerun()

render_board()

st.markdown(
    '<div class="small-note">Choose the arrow above a column to drop your coin.</div>',
    unsafe_allow_html=True,
)

if st.session_state.turn == COMPUTER and not st.session_state.game_over:
    with st.spinner("AI is thinking..."):
        column, _score = get_ai_move(
            st.session_state.board,
            depth=st.session_state.depth,
            computer_coin=COMPUTER,
        )
        if column is not None:
            play_move(column, COMPUTER)
    if not st.session_state.game_over:
        st.session_state.turn = PLAYER
    st.rerun()

st.write("")
m1, m2, m3 = st.columns(3)
m1.metric("Moves played", st.session_state.moves)
m2.metric("Open columns", len(get_valid_locations(st.session_state.board)))
m3.metric("Search depth", st.session_state.depth)

if st.session_state.game_over:
    if st.button("Play Again", use_container_width=True):
        new_game(True)
        st.rerun()
