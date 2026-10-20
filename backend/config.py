"""
ScholarTrack - Database Configuration

Responsibilities:
1. Load database configuration from environment variables.
2. Validate required settings.
3. Provide MySQL connection settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path


# --------------------------------------------------
# 1. Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)


# --------------------------------------------------
# 2. Application Configuration
# --------------------------------------------------

class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")

    DEBUG = False

    TESTING = False


# --------------------------------------------------
# 3. Database Configuration
# --------------------------------------------------

class DatabaseConfig:
    """MySQL connection configuration."""

    HOST = os.getenv("DB_HOST", "localhost")

    PORT = int(os.getenv("DB_PORT", "3306"))

    DATABASE = os.getenv("DB_NAME", "scholartrack_db")

    USER = os.getenv("DB_USER", "root")

    PASSWORD = os.getenv("DB_PASSWORD", "")

    CHARSET = "utf8mb4"

    CONNECT_TIMEOUT = 10

    READ_TIMEOUT = 10

    WRITE_TIMEOUT = 10

    @classmethod
    def get_connection_settings(cls):
        """
        Return MySQL connection settings.

        Raises:
            ValueError: If mandatory database settings are missing.
        """

        if not cls.HOST:
            raise ValueError("DB_HOST is missing in .env")

        if not cls.DATABASE:
            raise ValueError("DB_NAME is missing in .env")

        if not cls.USER:
            raise ValueError("DB_USER is missing in .env")

        if not cls.PASSWORD:
            raise ValueError(
                "DB_PASSWORD is missing in .env. "
                "Configure your MySQL password."
            )

        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "database": cls.DATABASE,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "charset": cls.CHARSET,
            "connect_timeout": cls.CONNECT_TIMEOUT,
            "read_timeout": cls.READ_TIMEOUT,
            "write_timeout": cls.WRITE_TIMEOUT,
            "autocommit": False
        }


# --------------------------------------------------
# 4. Development Configuration
# --------------------------------------------------

class DevelopmentConfig(Config):
    """Configuration for local development."""

    DEBUG = False


# --------------------------------------------------
# 5. Testing Configuration
# --------------------------------------------------

class TestingConfig(Config):
    """Configuration for automated tests."""

    TESTING = True


# --------------------------------------------------
# 6. Production Configuration
# --------------------------------------------------

class ProductionConfig(Config):
    """Configuration for production deployment."""

    DEBUG = False


# --------------------------------------------------
# 7. Configuration Mapping
# --------------------------------------------------

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}


# --------------------------------------------------
# 8. Get Configuration
# --------------------------------------------------

def get_config(environment=None):
    """
    Return the configuration class for the selected environment.
    """

    if environment is None:
        environment = os.getenv(
            "FLASK_ENV",
            "development"
        )

    selected_config = config_by_name.get(
        environment.lower()
    )

    if selected_config is None:
        raise ValueError(
            f"Unsupported environment: {environment}"
        )

    return selected_configcontinue
