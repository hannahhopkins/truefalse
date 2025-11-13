import streamlit as st
import pandas as pd
import random

@st.cache_data
def load_data():
    df = pd.read_csv("truefalse.csv")
    df.columns = [c.lower().strip() for c in df.columns]
    return df

df = load_data()

st.set_page_config(page_title="True/False Quiz", layout="wide")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    df = pd.read_csv("truefalse.csv")
    df.columns = [c.lower().strip() for c in df.columns]
    return df

df = load_data()

# ---- INITIALIZE SESSION STATE ----
if "order" not in st.session_state:
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)

if "index" not in st.session_state:
    st.session_state.index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "show_context" not in st.session_state:
    st.session_state.show_context = False

if "last_correct" not in st.session_state:
    st.session_state.last_correct = False

# ---- RESET FUNCTION ----
def restart_quiz():
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.show_context = False
    st.session_state.last_correct = False

# ---- UI HEADER ----
st.title("True or False Game")

# ---- BOTTOM-RIGHT SCORE DISPLAY ----
score_placeholder = st.empty()
score_placeholder.markdown(
    f"""
    <div style="position:fixed; bottom:20px; right:20px; 
                background:#f0f0f0; padding:12px 18px; 
                border-radius:10px; font-size:18px;">
        Score: <strong>{st.session_state.score}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- END OF QUIZ ----
if st.session_state.index >= len(st.session_state.order):
    st.success(f"🎉 Quiz complete! Final score: {st.session_state.score}/{len(df)}")

    if st.button("Play Again"):
        restart_quiz()

    st.stop()

# ---- GET CURRENT QUESTION ----
q_idx = st.session_state.order[st.session_state.index]
row = df.iloc[q_idx]

statement = row["statement"]
correct_answer = str(row["outcome"]).strip().lower()
context = row.get("context", "")

# ---- QUESTION DISPLAY ----
st.markdown(f"### {statement}")

# ---- BUTTON HANDLING ----
# ---- BUTTON LAYOUT (LARGE, COLORED) ----

# Custom CSS for button styling
st.markdown("""
<style>
.true-btn {
    background-color: #90EE90 !important;   /* light green */
    color: black !important;
    padding: 20px 40px !important;
    font-size: 24px !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
}
.false-btn {
    background-color: #FF6961 !important;   /* red */
    color: white !important;
    padding: 20px 40px !important;
    font-size: 24px !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
}
button[kind="secondary"] {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    true_clicked = st.button("✓ True", key=f"true_{st.session_state.index}", use_container_width=True)
    st.markdown(f"""
        <script>
        var btn = window.parent.document.querySelector('button[data-testid="baseButton-true_{st.session_state.index}"]');
        if (btn) {{
            btn.className += " true-btn";
        }}
        </script>
    """, unsafe_allow_html=True)

with col2:
    false_clicked = st.button("✗ False", key=f"false_{st.session_state.index}", use_container_width=True)
    st.markdown(f"""
        <script>
        var btn = window.parent.document.querySelector('button[data-testid="baseButton-false_{st.session_state.index}"]');
        if (btn) {{
            btn.className += " false-btn";
        }}
        </script>
    """, unsafe_allow_html=True)

# Handle logic
if true_clicked:
    handle_answer("true")

if false_clicked:
    handle_answer("false")

# ---- FEEDBACK AFTER ANSWERING ----
if st.session_state.answered:
    if st.session_state.last_correct:
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is **{correct_answer.title()}**.")

    if isinstance(context, str) and context.strip():
        st.info(f"**Context:** {context}")

    if st.button("Next Question ➜"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.show_context = False
        st.session_state.last_correct = False
        st.rerun()

