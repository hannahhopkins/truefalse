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


# ---- SAFE CSS-ONLY BUTTON STYLING ----
st.markdown("""
<style>
/* TRUE BUTTON STYLE */
button.true-btn {
    background-color: #90EE90 !important; /* Light green */
    color: black !important;
    padding: 20px !important;
    font-size: 24px !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
}

/* FALSE BUTTON STYLE */
button.false-btn {
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
    st.markdown("## 🎉 Quiz complete!")
    st.write(f"Final score: **{st.session_state.score} / {len(df)}**")

    if st.button("Play Again"):
        restart_quiz()
        st.rerun()

    st.stop()


# ---- CURRENT QUESTION ----
q_idx = st.session_state.order[st.session_state.index]
row = df.iloc[q_idx]

statement = row["statement"]
correct_answer = str(row["outcome"]).strip().lower()

# ---- SAFE CONTEXT HANDLING ----
raw_context = row.get("context", "")

if isinstance(raw_context, float) or raw_context is None:
    context = ""
else:
    context = str(raw_context).strip()



# ---- TITLE (H1) ----
st.markdown("# True or False?")

# ---- STATEMENT (H2) ----
st.markdown(f"## {statement}")


# ---- BUTTONS ----
col1, col2 = st.columns(2)

with col1:
    true_btn = st.button("✓ True", key=f"true_{st.session_state.index}")
with col2:
    false_btn = st.button("✗ False", key=f"false_{st.session_state.index}")

# Assign CSS classes safely AFTER creation
st.markdown(
    f"""
    <script>
    const parent = window.parent.document;

    let t = parent.querySelector('button[data-testid="baseButton-true_{st.session_state.index}"]');
    if (t) t.classList.add('true-btn');

    let f = parent.querySelector('button[data-testid="baseButton-false_{st.session_state.index}"]');
    if (f) f.classList.add('false-btn');
    </script>
    """,
    unsafe_allow_html=True
)


# ---- ANSWER LOGIC ----
def handle_answer(choice):
    if st.session_state.answered:
        return

    st.session_state.answered = True

    if choice == correct_answer:
        st.session_state.score += 1
        st.session_state.last_correct = True
    else:
        st.session_state.last_correct = False


if true_btn:
    handle_answer("true")

if false_btn:
    handle_answer("false")


# ---- FEEDBACK ----
if st.session_state.answered:
    if st.session_state.last_correct:
        st.success("Correct!")
    else:
        st.error(f"Incorrect — the correct answer is **{correct_answer.title()}**.")

    if context and context.lower() != "nan":
        st.info(f"**Context:** {context}")

    if st.button("Next Question ➜"):
        st.session_state.index += 1
        st.session_state.answered = False
        st.rerun()
