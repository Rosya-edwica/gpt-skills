import pymysql
from models import Pair
import os


def connect() -> pymysql.connections.Connection:
    connection = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_NAME")
    )
    return connection


def get_skill_pair() -> Pair | None:
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT id, demand_name, dup_demand_name, is_duplicate
    FROM demand_duplicate
    WHERE is_duplicate_gpt IS NULL
    LIMIT 1""")
    data = cursor.fetchone()
    connection.close()
    if not data:
        return None
    else:
        return Pair(*data)


def update_row(pair) -> None:
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE demand_duplicate
        SET is_duplicate_gpt = {pair.IsDuplicate}
        WHERE id = {pair.Id}
    """)
    connection.commit()
    connection.close()
