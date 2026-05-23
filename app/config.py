from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API Clasificacion Enfermedades Papa"
    app_version: str = "1.0.0"
    model_path: str = "ensamble_papa_completo_compatible_dynamic.tflite"
    database_url: str = "sqlite:///./potato_diseases.db"
    model_input_width: int = 224
    model_input_height: int = 224
    cors_origins: str = "*"
    class_names: tuple[str, str, str] = ("Early_Blight", "Healthy", "Late_Blight")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
