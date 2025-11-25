from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #base de datos y seguridad
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    #configuracion de email
    SMTP_SERVER: str 
    SMTP_PORT: int
    SENDER_EMAIL: str
    SENDER_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" 
    )

settings = Settings()