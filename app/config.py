from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostame: str
    database_port: str
    database_name: str
    algorithm: str
    access_token_expire_mins: int
    database_password: str
    database_username:str 
    sercret_key:str
    class Config:
        env_file = ".env"

settings = Settings()