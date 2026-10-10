import os

from flask import Flask

from config import Config, DevelopmentConfig, TestingConfig
from error_handlers import register_error_handlers
from routes.admin_routes import admin_bp
from routes.products_routes import api_bp
from utils.db import mysql

CONFIGS = {
    "production": Config,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        environment = os.getenv("APP_ENV", "production").lower()
        config_object = CONFIGS.get(environment)

        if config_object is None:
            raise RuntimeError(f"APP_ENV no reconocido: {environment}")

    app.config.from_object(config_object)

    # Validar configuración antes de inicializar MySQL.
    if hasattr(config_object, "validate"):
        config_object.validate(app.config)

    mysql.init_app(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])
