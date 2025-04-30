from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    token: str
    url: str

    @property
    def get_token(self):
        return self.token
    def get_url(self):
        return self.url
    model_config = SettingsConfigDict(env_file="TGbot/.env")

settings = Settings()