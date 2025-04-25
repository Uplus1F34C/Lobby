from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    token: str

    @property
    def get_token(self):
        return self.token
    model_config = SettingsConfigDict(env_file="TGbot/.env")

settings = Settings()