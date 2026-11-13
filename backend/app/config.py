import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
load_dotenv(PROJECT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    image_model: str
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    allowed_origins: tuple[str, ...]
    upload_directory: Path
    demo_image_directory: Path

    @classmethod
    def from_environment(cls):
        origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173")

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            image_model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.5-sunburst"),
            mysql_host=os.getenv("MYSQL_HOST", "db"),
            mysql_port=int(os.getenv("MYSQL_PORT", "3306")),
            mysql_database=os.getenv("MYSQL_DATABASE", "casa_forma"),
            mysql_user=os.getenv("MYSQL_USER", "casa_forma"),
            mysql_password=os.getenv("MYSQL_PASSWORD", ""),
            allowed_origins=tuple(origin.strip() for origin in origins.split(",") if origin.strip()),
            upload_directory=Path(
                os.getenv("UPLOAD_DIR", str(BACKEND_DIR / "uploads"))
            ).resolve(),
            demo_image_directory=Path(__file__).resolve().parent / "demo_images",
        )
