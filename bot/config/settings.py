from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    works_client_id: str
    works_client_secret: str
    bot_secret: str
    bot_id: str
    private_key_path: str
    service_account: str

    class Config:
        env_file = ".env"


settings = Settings()
