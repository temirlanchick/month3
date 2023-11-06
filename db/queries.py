import sqlite3
from pathlib import Path
from pprint import pprint


# DBMS - СУБД


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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            productsId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            image TEXT,
            categoryId INTEGER,
            FOREIGN KEY (categoryId) REFERENCES categories(categoryId)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS questionaire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            country TEXT
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


def get_products_by_category(category_id: int):
    cursor.execute(f"SELECT * FROM products WHERE categoryId = {category_id}")
    return cursor.fetchall()


def get_products_by_category_name(category_name: str):
    cursor.execute(
        f"""SELECT * FROM products WHERE categoryId = (
            SELECT categoryId FROM categories WHERE name = '{category_name}'
        )"""
    )
    return cursor.fetchall()


def save_question(data):
    print(data)
    cursor.execute(
        """
        INSERT INTO questionaire (name, age, gender, country)
        VALUES (:name, :age, :gender, :country)
        """,
        {
            "name": data["name"],
            "age": data["age"],
            "gender": data["gender"],
            "country": data["country"],
        },
    )
    db.commit()


if __name__ == "__main__":
    init_db()
    create_tables()
    populate_tables()
    pprint(get_all_products())
    # pprint(get_products_by_category(3))
    # pprint(get_products_by_category_name("Манга"))

# таблица Categories
# 1, "Книги", "Книги - это творческая литература",
# 2, "Сувениры", "Сувениры - это ....."
# 3, "Манга", "Манга - это ....."

# таблица Products
# 1, 'Книга 1', 100.0, 'images/book.jpg', 1
# 2, 'Книга 2', 200.0, 'images/book.jpg', 1
# 3, "Сувенир 1", 100.0, "images/souvenir.jpg", 2
# Foreign Key - Внешний ключ
