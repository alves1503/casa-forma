from ..config import Settings
from .database import connect


def seed_admin(settings: Settings, username: str, password_hash: str):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS count FROM admin_users")
            if cursor.fetchone()["count"]:
                return
            cursor.execute(
                "INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash),
            )


def get_admin_user(settings: Settings, username: str):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username, password_hash FROM admin_users WHERE username = %s",
                (username,),
            )
            return cursor.fetchone()


def update_admin_password(settings: Settings, username: str, password_hash: str):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE admin_users SET password_hash = %s WHERE username = %s",
                (password_hash, username),
            )
            return cursor.rowcount > 0
