from config import settings
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, InputMediaPhoto
import os


class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
    
    async def send_photo(self, chat_id: int | str, photo: str | bytes, caption: str = "", **kwargs):
        if isinstance(photo, str) and photo.startswith(("http://", "https://")):
            return await self.bot.send_photo(chat_id, photo, caption=caption, **kwargs)
        return await self.bot.send_photo(chat_id, InputFile(photo), caption=caption, **kwargs)

    async def send_photos(self, chat_id: int | str, photos: list, captions: list = None, **kwargs):
        media = []
        for i, photo in enumerate(photos):
            caption = captions[i] if captions and i < len(captions) else ""
            if isinstance(photo, str) and photo.startswith(("http://", "https://")):
                media.append(InputMediaPhoto(media=photo, caption=caption))
            else:
                media.append(InputMediaPhoto(media=InputFile(photo), caption=caption))
        return await self.bot.send_media_group(chat_id, media, **kwargs)

    async def download_photo(self, photo: types.PhotoSize, save_dir: str = "photos") -> str:
        os.makedirs(save_dir, exist_ok=True)
        file = await self.bot.get_file(photo.file_id)
        file_path = os.path.join(save_dir, f"{file.file_id}.jpg")
        await self.bot.download_file(file.file_path, file_path)
        return file_path

    async def send_message(self, chat_id: int | str, text: str, **kwargs) -> types.Message:
        return await self.bot.send_message(chat_id, text, **kwargs)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)

    async def close(self):
        await self.bot.session.close()

bot = TelegramBot(settings.TG_TOKEN)