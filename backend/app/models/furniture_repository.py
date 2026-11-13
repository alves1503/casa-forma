from ..config import Settings
from .database import connect
from .furniture import FURNITURE


def seed_furniture(settings: Settings):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS count FROM furniture")
            if cursor.fetchone()["count"]:
                return
            cursor.executemany(
                """
                INSERT INTO furniture
                    (id, name, category, description, color, reference_alt, prompt, photo_path)
                VALUES
                    (%(id)s, %(name)s, %(category)s, %(description)s, %(color)s,
                     %(reference_alt)s, %(prompt)s, %(photo_path)s)
                """,
                FURNITURE,
            )


def get_all_furniture(settings: Settings):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM furniture ORDER BY created_at, id")
            return cursor.fetchall()


def get_furniture(settings: Settings, furniture_id: str):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM furniture WHERE id = %s", (furniture_id,))
            return cursor.fetchone()


def update_furniture_photo(settings: Settings, furniture_id: str, photo_path: str):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE furniture SET photo_path = %s, is_demo = FALSE WHERE id = %s",
                (photo_path, furniture_id),
            )
            return cursor.rowcount > 0
