from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST:  str
    DB_USER:  str
    DB_PASS:  str
    DB_NAME:  str
    DB_PORT:  int
    TG_TOKEN: str
    VK_TOKEN: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    @property
    def VK_GROUP_DOMAIN(self):
        return "offtrinityrpg"
    
    @property
    def TG_CHAT_ID(self):
        return -1002611839532
    
    @property
    def LOG_CHAT_ID(self):
        return -1002644900239
    
    @property
    def ADMIN_LIST(self):
        return [697261219, 7592996281, 7651698093, 903160137, 305356170, 1570109707]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()