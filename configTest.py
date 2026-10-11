import os


class TestingConfig:
    DEBUG = False
    TESTING = True
    PROPAGATE_EXCEPTIONS = False

    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "integration-test-secret")
    MYSQL_HOST = os.getenv("TEST_MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.getenv("TEST_MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("TEST_MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("TEST_MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("TEST_MYSQL_DATABASE", "restaurantdb")


config = {"testing": TestingConfig}
