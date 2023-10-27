def populate_tables():
    cursor.execute(
        """
        INSERT INTO categories (name)
        VALUES ('Игры'),
               ('Скины'),
               ('Оружие')
        """
    )
    cursor.execute(
        """
        INSERT INTO game (name, price, image, categoryId)
        VALUES ('Assasins Creed 3', 100.0, 'images/book.jpg', 1),
               ('Far Cry 5', 200.0, 'images/book.jpg', 1),
               ('Наряд Эцио', 300.0, 'images/book.jpg', 2),
               ('Наряд Альтаира', 400.0, 'images/book.jpg', 2),
               ('Клинок', 1000.0, 'images/clinoc.jpg', 3)
               ('Арбалет', 2000.0, 'images/arbalet.jpg', 3)
        """
    )

    db.commit()


def get_all_games():
    cursor.execute(
        "SELECT p.productsId, p.name, c.name FROM products AS p JOIN categories AS c ON p.categoryId = c.categoryId"
    )
    return cursor.fetchall()


def get_games_by_category(category_id: int):
    cursor.execute(f"SELECT * FROM game WHERE categoryId = {category_id}")
    return cursor.fetchall()


def get_games_by_category_name(category_name: str):
    cursor.execute(
        f"""SELECT * FROM game WHERE categoryId = (
            SELECT categoryId FROM categories WHERE name = '{category_name}'
        )"""
    )
    return cursor.fetchall()


if __name__ == "__main__":
    init_db()
    create_tables()
    populate_tables()
    print(get_all_games())
    print(get_games_by_category())
    print(get_games_by_category_name('Оружие'))