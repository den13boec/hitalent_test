import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="forbid"
    )

    database_url: str | None = None
    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "qna"
    postgres_user: str = "qna"
    postgres_password: str | None = None
    postgres_password_file: str | None = None

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        pwd = self.postgres_password
        if (
            not pwd
            and self.postgres_password_file
            and os.path.exists(self.postgres_password_file)
        ):
            with open(self.postgres_password_file, "r", encoding="utf-8") as f:
                pwd = f.read().strip()
        if not pwd:
            raise RuntimeError("No DB password provided")
        return f"postgresql+psycopg2://{self.postgres_user}:{pwd}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
