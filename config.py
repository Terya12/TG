from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_address: str
    db_name: str
    token: str

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_address}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
