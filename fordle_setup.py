import os
from sqlalchemy import create_engine

MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_DB = os.environ.get("MYSQL_DB")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)  # default 3306

connection_string = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_string)
