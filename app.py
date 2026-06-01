import streamlit as st
import numpy as np

st.set_page_config(page_title="Tic Tac Toe", page_icon="🕹️", layout="centered")

st.markdown("""
    <style>
    .main .block-container {
        max-width: 450px !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 20px;
    }
    
    div[data-testid="stButton"] > button {
        width: 100% !important;
        aspect-ratio: 1 / 1; 
        height: auto !important; 
        border-radius: 12px;
        background-color: #1e1e2f; 
        border: 2px solid #33334d;
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
        padding: 0 !important;
    }
    div[data-testid="stButton"] > button p {
        font-size: 5rem !important; 
        font-weight: bold !important;
        color: #ffffff !important;  
        margin: 0 !important;
        line-height: 1 !important;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #00eaee;
        background-color: #2a2a40;
    }
    div[data-testid="stButton"] > button:disabled {
        background-color: #161622;
        border: 2px solid #27273a;
        opacity: 1 !important; 
    }
    div[data-testid="stButton"] > button:disabled p {
        color: #ffffff !important; 
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🕹️Tic Tac Toe</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by NumPy & Streamlit</p>", unsafe_allow_html=True)

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1       
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.win_type = None  

svg_lines = {
    'row_0': '<line x1="2%" y1="16.5%" x2="98%" y2="16.5%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'row_1': '<line x1="2%" y1="50%" x2="98%" y2="50%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'row_2': '<line x1="2%" y1="83.5%" x2="98%" y2="83.5%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'col_0': '<line x1="16.5%" y1="2%" x2="16.5%" y2="98%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'col_1': '<line x1="50%" y1="2%" x2="50%" y2="98%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'col_2': '<line x1="83.5%" y1="2%" x2="83.5%" y2="98%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'diag_1': '<line x1="2%" y1="2%" x2="98%" y2="98%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
    'diag_2': '<line x1="2%" y1="98%" x2="98%" y2="2%" stroke="#ff4b4b" stroke-width="15" stroke-linecap="round" />',
}

def check_winner(b):
    for i in range(3):
        if abs(np.sum(b[i,:])) == 3: return ('X' if b[i,0] == 1 else 'O', f'row_{i}')
    for i in range(3):
        if abs(np.sum(b[:,i])) == 3: return ('X' if b[0,i] == 1 else 'O', f'col_{i}')
    if abs(np.trace(b)) == 3: return ('X' if b[0,0] == 1 else 'O', 'diag_1')
    if abs(np.trace(np.fliplr(b))) == 3: return ('X' if b[0,2] == 1 else 'O', 'diag_2')
    if not 0 in b: return ('Draw', None)
    return (None, None)

def make_move(row, col):
    if st.session_state.board[row, col] == 0 and not st.session_state.game_over:
        st.session_state.board[row, col] = st.session_state.current
        
        winner, win_type = check_winner(st.session_state.board)
        if winner is not None:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.win_type = win_type
        else:
            st.session_state.current *= -1

def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.win_type = None

# Status Display
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.warning("🤝 It's a Tie!")
    else:
        st.balloons()
        st.success(f"🎉 Player {st.session_state.winner} takes the victory!")
else:
    current_player = 'X' if st.session_state.current == 1 else 'O'
    st.info(f"👉 **{current_player}**'s turn to play")

st.write("") 

symbols = {0: "\u200b", 1: "X", -1: "O"} 

# FIXED HTML/CSS Section: No extra indentation to prevent Markdown code block rendering
if st.session_state.game_over:
    html_board = '<div style="position: relative; max-width: 450px; margin: auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">\n'
    
    for r in range(3):
        for c in range(3):
            val = st.session_state.board[r, c]
            symbol = "X" if val == 1 else "O" if val == -1 else ""
            html_board += f'<div style="aspect-ratio: 1; background-color: #161622; border: 2px solid #27273a; border-radius: 12px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 5rem; font-weight: bold; color: #ffffff; line-height: 1;">{symbol}</span></div>\n'
            
    if st.session_state.win_type:
        html_board += f'<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10;">{svg_lines[st.session_state.win_type]}</svg>\n'
        
    html_board += '</div>'
    
    st.markdown(html_board, unsafe_allow_html=True)

else:
    for r in range(3):
        cols = st.columns(3, gap="small") 
        for c in range(3):
            val = st.session_state.board[r, c]
            with cols[c]:
                st.button(
                    label=symbols[val],
                    key=f"cell_{r}_{c}",
                    on_click=make_move,
                    args=(r, c),
                    disabled=bool(val != 0),
                    use_container_width=True
                )

st.write("")

# Restart Button
with st.form("reset_form", border=False):
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        st.form_submit_button("🔄 Play Again", on_click=reset_game, use_container_width=True)