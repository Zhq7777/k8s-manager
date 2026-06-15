"""Configuration management"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Application info
    APP_NAME: str = "K8s Manager"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # K8s configuration
    KUBECONFIG_PATH: str | None = None
    IN_CLUSTER: bool = False

    # API configuration
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    # Database configuration
    DATABASE_URL: str = "sqlite:///./k8s_manager.db"

    # Security configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
