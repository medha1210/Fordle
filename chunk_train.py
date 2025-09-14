import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import joblib

MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_DB = os.environ.get("MYSQL_DB")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)  

connection_string = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_string)

solutions = pd.read_sql("SELECT word FROM valid_solutions", engine)['word'].str.lower().tolist()

letters = list("abcdefghijklmnopqrstuvwxyz")
letter_to_idx = {ch: i for i, ch in enumerate(letters)}

def encode_word(word):
    """Encode a 5-letter word as a 5x26 one-hot vector flattened"""
    mat = np.zeros((5, 26), dtype=int)
    for pos, ch in enumerate(word):
        mat[pos, letter_to_idx[ch]] = 1
    return mat.flatten()

# Prepare training data
X = np.array([encode_word(w) for w in solutions])
y = np.zeros((len(solutions), 26), dtype=int)

# Target: which letters appear in the word
for i, w in enumerate(solutions):
    for ch in set(w):
        y[i, letter_to_idx[ch]] = 1

# Train multi-output classifier
print("Model in training")
clf = MultiOutputClassifier(RandomForestClassifier(n_estimators=200, random_state=42))
clf.fit(X, y)
print("Model trained!\n")

# Save the model
joblib.dump(clf, "fordle_ml.pkl")
print("Saved model")
