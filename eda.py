import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DB")
)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS solution_difficulty AS
SELECT 
    TRIM(s.word) AS answer,
    AVG(CAST(g.Trial AS UNSIGNED)) AS avg_guesses,
    COUNT(*) AS plays
FROM games_raw g
JOIN valid_solutions s 
    ON TRIM(g.target) = TRIM(s.word)
GROUP BY TRIM(s.word);
"""
try:
    cursor.execute(query)
    conn.commit()
except mysql.connector.errors.ProgrammingError:
    # Table already exists, ignore creation
    pass


print("\nSample from solution_difficulty")
cursor.execute("SELECT * FROM solution_difficulty LIMIT 10;")
for row in cursor.fetchall():
    print(row)

# 5 easiest words
print("\nTop 5 easiest words to guess")
query = """
SELECT answer, ROUND(avg_guesses, 2), plays
FROM solution_difficulty
WHERE plays > 50
ORDER BY avg_guesses ASC
LIMIT 5;
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# 5 hardest words
print("\nTop 5 hardest words to guess")
query = """
SELECT answer, ROUND(avg_guesses, 2), plays
FROM solution_difficulty
WHERE plays > 50
ORDER BY avg_guesses DESC
LIMIT 5;
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# Failed words
print("\n10 words most often failed to guess")
query = """
SELECT TRIM(s.word) AS answer, COUNT(*) AS fails
FROM games_raw g
JOIN valid_solutions s 
    ON TRIM(g.target) = TRIM(s.word)
WHERE g.Trial >= 6
GROUP BY TRIM(s.word)
HAVING COUNT(*) > 50
ORDER BY fails DESC
LIMIT 10;
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# Most frequently guessed words
print("\nTop 10 most frequently guessed words")
query = """
SELECT answer, ROUND(avg_guesses, 2), plays
FROM solution_difficulty
ORDER BY plays DESC
LIMIT 10;
"""
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
