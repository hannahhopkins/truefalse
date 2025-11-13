import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="True/False Quiz", layout="wide")

# ---- LOAD CSV ----
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

if "last_correct" not in st.session_state:
    st.session_state.last_correct = False


# ---- RESET FUNCTION ----
def restart_quiz():
    st.session_state.order = list(range(len(df)))
    random.shuffle(st.session_state.order)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_correct = False


# ---- CSS OVERRIDES FOR LARGE COLORED BUTTONS ----
st.markdown("""
<style>

button[kind="secondary"] {
    background-color: transparent !important;
}

/* TRUE BUTTON */
div[data-testid="column"]:nth-of-type(1) button {
    background-color: #90EE90 !important; /* Light green */
    color: black !important;
    padding: 20px !important;
    font-size: 24px !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
}

/* FALSE BUTTON */
div[data-testid="column"]:nth-of-type(2) button {
    background-color: #FF6961 !important; /* Red */
    color: white !important;
    padding: 20px !important;
    font-size: 24px !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
}

</style>
""", unsafe_allow_html=True)


# ---- FLOATING SCORE BADGE ----
score_html = """
<div style="position:fixed; bottom:20px; right:20px; 
            background:#f0f0f0; padding:12px 18px; 
            border-radius:10px; font-size:18px; 
            box-shadow: 0 0 5px rgba(0,0,0,0.3);">
    Score: <strong>{}</strong>
</div>
""".format(st.session_state.score)

st.markdown(score_html, unsafe_allow_html=True)


# ---- END OF QUIZ ----
if st.session_state.index >= len(st.session_state.order):
    st.success(f"🎉 Quiz complete! Final score: {st.session_state.score}/{len(df)}")

    if st.button("Play Again"):
        restart_quiz()
        st.rerun()

    st.stop()


# ---- GET CURRENT QUESTION ----
q_idx = st.session_state.order[st.session_state.index]
row = df.iloc[q_idx]

statement = row["statement"]
correct_answer = str(row["outcome"]).strip().lower()
context = row.get("context", "")


# ---- SHOW QUESTION ----
st.markdown(f"## {statement}")


# ---- BUTTONS ----
col1, col2 = st.columns(2)

with col1:
    true_clicked = st.button("✓ True", key=f"true_{st.session_state.index}")

with col2:
    false_clicked = st.button("✗ False", key=f"false_{st.session_state.index}")


# ---- ANSWER HANDLING ----
def handle_answer(choice):
    if st.session_state.answered:
        return

    st.session_state.answered = True

    if choice == correct_answer:
        st.session_state.score += 1
        st.session_state.last_correct = True
    else:
        st.session_state.last_correct = False


if true_clicked:
    handle_answer("true")

if false_clicked:
    handle_answer("false")


# ---- FEEDBACK ----
if st.session_state.answered:
    if st.session_state.last_correct:
        st.success("Correct!")
    else:
        st.error(f"Incorrect — the correct answer is **{correct_answer.title()}**.")

    if isinstance(context, str) and context.strip() and context.lower() != "nan":
        st.info(f"**Context:** {context}")

    if st.button("Next Question ➜"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.rerun()
