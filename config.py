import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DATABASE")

    DEBUG = False
    TESTING = False

    @classmethod
    def validate(cls, config):
        required = (
            "SECRET_KEY",
            "MYSQL_HOST",
            "MYSQL_USER",
            "MYSQL_PASSWORD",
            "MYSQL_DB",
        )

        missing = [key for key in required if not config.get(key)]

        if missing:
            raise RuntimeError(
                "Faltan variables de configuración: " + ", ".join(missing)
            )

        port = config.get("MYSQL_PORT")

        if not isinstance(port, int) or not 1 <= port <= 65535:
            raise RuntimeError("MYSQL_PORT está fuera de rango")


class DevelopmentConfig(Config):
    DEBUG = os.getenv("FLASK_DEBUG", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
