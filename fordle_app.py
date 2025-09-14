import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import joblib

letters = list("abcdefghijklmnopqrstuvwxyz")
letter_to_idx = {ch: i for i, ch in enumerate(letters)}
color_map = {"Black": "b", "Yellow": "y", "Green": "g"}
square_colors = {"b": "#787c7e", "y": "#c9b458", "g": "#6aaa64"}
MODEL_PATH = "fordle_ml.pkl"
SOLUTIONS_PATH = "valid_solutions.csv"  


@st.cache_data
def load_solutions():
    df = pd.read_csv(SOLUTIONS_PATH)
    return df['word'].str.lower().tolist()

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

solutions = load_solutions()
clf = load_model()


def encode_word(word):
    mat = np.zeros((5, 26), dtype=int)
    for pos, ch in enumerate(word):
        mat[pos, letter_to_idx[ch]] = 1
    return mat.flatten()

def filter_words(words, guess, feedback):
    guess = guess.lower()
    feedback = feedback.lower()
    result = []

    confirmed_counts = Counter()
    for g, f in zip(guess, feedback):
        if f in 'gy':
            confirmed_counts[g] += 1

    for word in words:
        word_counter = Counter(word)
        ok = True
        used_counts = Counter()
        for i, (g, f) in enumerate(zip(guess, feedback)):
            if f == 'g':
                if word[i] != g:
                    ok = False
                    break
                used_counts[g] += 1
            elif f == 'y':
                if g not in word or word[i] == g:
                    ok = False
                    break
                used_counts[g] += 1
            elif f == 'b':
                if word_counter[g] > confirmed_counts.get(g, 0):
                    ok = False
                    break
        if ok:
            result.append(word)
    return result

def rank_words_ml(candidates, clf):
    if not candidates:
        return []
    X_cand = np.array([encode_word(w) for w in candidates])
    proba = clf.predict_proba(X_cand)

    scores = []
    for i, word in enumerate(candidates):
        word_score = 0
        for j, ch in enumerate(word):
            word_score += proba[letter_to_idx[ch]][i][1]
        scores.append((word, word_score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return [w for w, s in scores[:10]]

# Streamlit UI
st.title("FORDLE! 🟩🟨⬛")

if "candidates" not in st.session_state:
    st.session_state.candidates = solutions[:]
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous guesses
st.subheader("Previous guesses")
for guess_word, feedback_str in st.session_state.history:
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.markdown(
            f"<div style='text-align:center;background-color:{square_colors[feedback_str[i]]};color:white;padding:10px;font-weight:bold;border-radius:5px'>{guess_word[i].upper()}</div>",
            unsafe_allow_html=True
        )

# Input new guess
st.subheader("Enter new guess")
guess = st.text_input("Guess (5 letters)").strip().lower()

# 5 squares for feedback
st.write("Select feedback for each letter:")
cols = st.columns(5)
feedback_list = []
for i, col in enumerate(cols):
    feedback_list.append(col.selectbox(f"Letter {i+1}", ["Black", "Yellow", "Green"], key=f"fb{i}"))

feedback = "".join([color_map[c] for c in feedback_list])

if st.button("Submit") and len(guess) == 5:
    st.session_state.candidates = filter_words(st.session_state.candidates, guess, feedback)
    st.session_state.history.append((guess, feedback))

    if not st.session_state.candidates:
        st.warning("No candidates left. Maybe feedback was wrong. Resetting candidates.")
        st.session_state.candidates = solutions[:]

    suggestions = rank_words_ml(st.session_state.candidates, clf)
    st.subheader(f"Top suggestions ({len(st.session_state.candidates)} possible words left):")
    st.write(", ".join(suggestions))
