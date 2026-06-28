from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # DATABASE
    # =========================
    DATABASE_URL: str

    # =========================
    # AUTH
    # =========================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    REFRESH_TOKEN_REMEMBER_DAYS: int = 30

    # =========================
    # GOOGLE OAUTH
    # (optional for now)
    # =========================
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    # =========================
    # ENVIRONMENT
    # =========================
    ENV: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()