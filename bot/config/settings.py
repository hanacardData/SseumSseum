from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    works_client_id: str
    works_client_secret: str
    bot_secret: str
    private_key_path: str
    service_account: str
    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
