from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor

from ..config import Settings


@contextmanager
def connect(settings: Settings):
    connection = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        charset="utf8mb4",
        cursorclass=DictCursor,
        connect_timeout=10,
        autocommit=False,
    )
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def create_tables(settings: Settings):
    with connect(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS furniture (
                    id VARCHAR(80) PRIMARY KEY,
                    name VARCHAR(160) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    color VARCHAR(80) NOT NULL,
                    reference_alt VARCHAR(180) NOT NULL,
                    prompt TEXT NOT NULL,
                    photo_path VARCHAR(255) NOT NULL,
                    is_demo BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_users (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """
            )
