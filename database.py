import sqlite3

DB_PATH = "database/games.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT UNIQUE,

        store TEXT,

        original_price REAL,

        deal_price REAL,

        currency TEXT,

        deal_price_inr REAL,

        discount REAL,

        rating INTEGER,

        image TEXT,

        url TEXT

    )
    """)

    connection.commit()
    connection.close()


def delete():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM games")

    connection.commit()
    connection.close()


def insert_game(
    title,
    store,
    original_price,
    deal_price,
    currency,
    deal_price_inr,
    discount,
    rating,
    image,
    url
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO games(

        title,
        store,
        original_price,
        deal_price,
        currency,
        deal_price_inr,
        discount,
        rating,
        image,
        url

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """, (

        title,
        store,
        original_price,
        deal_price,
        currency,
        deal_price_inr,
        discount,
        rating,
        image,
        url

    ))

    connection.commit()
    connection.close()

def filter_games(
    search="",
    sort="",
    store="",
    page=1,
    per_page=12
):

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM games"
    conditions = []
    parameters = []

    if search:
        conditions.append("title LIKE ?")
        parameters.append(f"%{search}%")

    if store:
        conditions.append("store = ?")
        parameters.append(store)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort == "low":
        query += " ORDER BY deal_price_inr ASC"

    elif sort == "high":
        query += " ORDER BY deal_price_inr DESC"

    elif sort == "discount":
        query += " ORDER BY discount DESC"

    elif sort == "rating":
        query += " ORDER BY rating DESC"

    else:
        query += " ORDER BY discount DESC"

    offset = (page - 1) * per_page

    query += " LIMIT ? OFFSET ?"

    parameters.extend([per_page, offset])

    cursor.execute(query, parameters)

    games = cursor.fetchall()

    connection.close()

    return games


def get_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM games")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(deal_price_inr),2) FROM games")
    average = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(deal_price_inr) FROM games")
    lowest = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(deal_price_inr) FROM games")
    highest = cursor.fetchone()[0]

    connection.close()

    return total, average, lowest, highest


def get_game_by_id(game_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

    SELECT *

    FROM games

    WHERE id=?

    """, (game_id,))

    game = cursor.fetchone()

    connection.close()

    return game


def get_all_games():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    SELECT *

    FROM games

    ORDER BY discount DESC

    """)

    games = cursor.fetchall()

    connection.close()

    return games


if __name__ == "__main__":

    create_table()

    rows = get_all_games()

    for row in rows:

        print(dict(row))