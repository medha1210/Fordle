import os
import mysql.connector
import pandas as pd

# MySQL connection
conn = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DB")
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS games_raw (
    game_number INT,
    user_id VARCHAR(50),
    score_text VARCHAR(10),
    created_at DATETIME
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS valid_guesses (
    guess VARCHAR(10)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS valid_solutions (
    game_number INT,
    answer VARCHAR(10)
);
""")

conn.commit()


cursor.execute("""
LOAD DATA LOCAL INFILE 'C:/Users/medha/OneDrive/Desktop/Fordle/wordle_games.csv'
INTO TABLE games_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
""")

cursor.execute("""
LOAD DATA LOCAL INFILE 'C:/Users/medha/OneDrive/Desktop/Fordle/valid_guesses.csv'
INTO TABLE valid_guesses
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
""")

cursor.execute("""
LOAD DATA LOCAL INFILE 'C:/Users/medha/OneDrive/Desktop/Fordle/valid_solutions.csv'
INTO TABLE valid_solutions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
""")

conn.commit()


cursor.execute("SELECT COUNT(*) FROM games_raw;")
print("games_raw count:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM valid_guesses;")
print("valid_guesses count:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM valid_solutions;")
print("valid_solutions count:", cursor.fetchone()[0])

cursor.close()
conn.close()
