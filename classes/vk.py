import aiohttp, logging
from classes.VkClasses import Wall
from config import settings
import json

API_URL = "https://api.vk.com/method/"

class VK:
    token: str
    v: str
    lang: str

    def __init__(self, token: str, v: str = "5.199", lang: str = "ru"):
        self.token = token
        self.v = v
        self.lang = lang

    async def wall_get(self, **params) -> list[Wall] | None:
        response = await self.request("wall.get", **params)
        if response == None:
            return None
        result: list[Wall] = []
        for elem in response['items']:
            result.append(Wall(**elem))
        return result


    async def request(self, method: str, **params) -> list | None:
        params['v'] = self.v
        params['lang'] = self.lang
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL+method, data=params, headers={"Authorization": f"Bearer {settings.VK_TOKEN}"}, ssl=False) as response:
                try:
                    vkr = await response.json()
                    if 'response' in vkr:
                        return vkr['response']
                except Exception as e:
                    logging.error("Vk response parse error. Raw: "+await response.text())
                    return None

