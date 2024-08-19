from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = ""
    secret_key: str = None
    algorithm: str = None
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = "a@a.com"
    mail_port: int = 0
    mail_server: str = ""
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = None
    cloudinary_api_key: str = None
    cloudinary_api_secret: str = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
