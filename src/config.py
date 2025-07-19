from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Clase para gestionar la configuración de la aplicación.
    Carga las variables desde un archivo .env si existe.
    """
    DATABASE_URL: str = 'postgresql://postgres:admin@localhost:5432/postgres'
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASS: str = "admin"

    # Permite cargar las variables desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Instancia única de la configuración que será usada en toda la aplicación
settings = Settings()