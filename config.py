from pydantic_settings import BaseSettings, SettingsConfigDict
import sys

class Settings(BaseSettings):
    DB_HOST:  str
    DB_USER:  str
    DB_PASS:  str
    DB_NAME:  str
    DB_PORT:  int
    TG_TOKEN: str
    TG_TOKEN_TEST: str
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
    
    @property
    def IS_TEST(self):
        return False
    
    @property
    def CHAT_THREAD_ID(self):
        return 1

    model_config = SettingsConfigDict(env_file=".env")

class SettingsTest(Settings):
    def __init__(self):
        super().__init__()
        self.TG_TOKEN = self.TG_TOKEN_TEST

    @property
    def TG_CHAT_ID(self):
        return -1002644900239

    @property
    def IS_TEST(self):
        return True
    
    @property
    def CHAT_THREAD_ID(self):
        return 330

    model_config = SettingsConfigDict(env_file=".env")


if "-test" in sys.argv:
    print("Loaded test settings")
    settings = SettingsTest()
else:
    print("Lodead production settings")
    settings = Settings()