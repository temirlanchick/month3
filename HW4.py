import sqlite3
from pathlib import Path
from pprint import pprint


def init_db():
    global db, cursor
    db = sqlite3.connect(Path(__file__).parent.parent / "db.sqlite3")
    cursor = db.cursor()


def create_tables():
    cursor.execute(
        """
        DROP TABLE IF EXISTS products
        """
    )
    cursor.execute(
        """
        DROP TABLE IF EXISTS categories
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            categoryId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """
    )


    db.commit()


def populate_tables():
    cursor.execute(
        """
        INSERT INTO categories (name)
        VALUES ('Книги'),
               ('Сувениры'),
               ('Манга')
        """
    )
    cursor.execute(
        """
        INSERT INTO products (name, price, image, categoryId)
        VALUES ('Книга 1', 100.0, 'images/book.jpg', 1),
               ('Книга 2', 200.0, 'images/book.jpg', 1),
               ('Книга 3', 300.0, 'images/book.jpg', 1),
               ('Манга Жизнь', 400.0, 'images/book.jpg', 3)
    """
    )
    db.commit()


def get_all_products():
    # ASC - по возрастанию ASCENDING
    # DESC - по убыванию DESCENDING
    cursor.execute(
        "SELECT p.productsId, p.name, c.name FROM products AS p JOIN categories AS c ON p.categoryId = c.categoryId"
    )
    return cursor.fetchall()




if __name__ == "__main__":
    init_db()
    create_tables()
    populate_tables()
    pprint(get_all_products())
