import asyncio
from classes.Storage import CacheStorage
from config import settings
from classes.bot import bot
from classes.vk import VK

POLL_DELAY = 60
CHECK_TIME = 60*60*5 # 5 chasov

vk = VK(settings.VK_TOKEN)
cache = CacheStorage("wall-posts")

async def get_vk_updates() -> list:
    wall = await vk.wall_get(domain=settings.VK_GROUP_DOMAIN, count=10)
    if wall:
        posted: list = cache.get()
        queue = []
        for post in wall:
            if post.id not in posted:
                queue.append(post)
        return queue

async def run():
    to_post = await get_vk_updates()
    if len(to_post) > 0:



    asyncio.sleep(POLL_DELAY)

