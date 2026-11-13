from .config import Settings
from .models.admin_repository import seed_admin
from .models.database import create_tables
from .models.furniture_repository import seed_furniture

SEED_ADMIN_USERNAME = "admin"
SEED_ADMIN_PASSWORD_HASH = (
    "pbkdf2_sha256$600000$eqq_bUOtPCX-rCxSl7gMYg$"
    "YdDF8_miaikg8D-d5IrE-VubJ5Q8_vXe4Gxn6JeFU8I"
)


def seed_database(settings: Settings):
    create_tables(settings)
    seed_furniture(settings)
    seed_admin(settings, SEED_ADMIN_USERNAME, SEED_ADMIN_PASSWORD_HASH)


if __name__ == "__main__":
    seed_database(Settings.from_environment())
    print("Tabelas e dados iniciais criados.")
