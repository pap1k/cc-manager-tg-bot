import asyncio, datetime, logging
from typing import Tuple
from classes.Storage import CacheStorage
from classes.CacheModels import PostCache, SkipWallPost
from config import settings
from classes.bot import bot
from classes.vk import VK
from classes.VkClasses import Wall
from helpers.fix_cache import fix_cache
from helpers.vk_to_tg import vk_to_tg
from helpers.send_log import AsyncRemoteHandler, send_to_remote

POLL_DELAY = 60
CHECK_TIME = 60*60*5 # 5 chasov

vk = VK(settings.VK_TOKEN)
cache = CacheStorage("wall-posts", PostCache, True)
skip_cache = CacheStorage("skip-wall-posts", SkipWallPost, True)

async def make_post(post: Wall):
    tg = vk_to_tg(post)
    if not tg:
        skip_data: list[SkipWallPost] = skip_cache.get()
        skip_data.append(SkipWallPost(vk_id=post.id))
        skip_cache.store(skip_data)
        return
    if tg.topic_id == -1:
        logging.info(f"[VK] Функция преобразования не определила тег, пропускаем")
        c = PostCache(vk_id=post.id, tg_id=0, post_time=post.date, last_edit=post.edited)
    else:
        logging.info(f"[VK] Выкладываем пост <{post.id}> в чат <{tg.chat_id}>, топик <{tg.topic_id}>")
        # TODO чето придумать с отправкой нескольких фото, а надо оно вообще или нет - хз
        if len(tg.attachments) > 0:
            resp = await bot.send_photo(tg.chat_id, tg.attachments[0], tg.text, message_thread_id = tg.topic_id)
        else:            
            resp = await bot.send_message(tg.chat_id, tg.text, message_thread_id = tg.topic_id, parse_mode="HTML", disable_web_page_preview=True)
        c = PostCache(vk_id=post.id, tg_id=resp.message_id, topic_id=resp.message_thread_id, post_time=post.date, last_edit=post.edited)

    current_cache: list[PostCache] = cache.get()
    current_cache.append(c)
    cache.store(current_cache)

async def edit_post(post: PostCache):
    post_cache: list[PostCache] = cache.get()
    for i in range(len(post_cache)):
        if post_cache[i].vk_id == post.vk_id:
            post_cache[i].last_edit = datetime.datetime.now()

async def get_vk_updates() -> Tuple[list[Wall], list[PostCache]]:
    wall = await vk.wall_get(domain=settings.VK_GROUP_DOMAIN, count=10)
    wall.reverse()
    if wall:
        posted: list[PostCache] = cache.get()
        skip_data: list[SkipWallPost] = skip_cache.get()
        queue_post = []
        queue_edit = []

        for post in wall:
            # Проверка новый постов
            # Проверка даты изменения поста по CHECK_TIME
            need_post = True
            chache_pointer = None
            for skip in skip_data:
                if skip.vk_id == post.id:
                    need_post = False

            for p in posted:
                if p.vk_id == post.id:
                    need_post = False
                    if post.edited:
                        if p.last_edit > post.edited:
                            chache_pointer = p
            
            if need_post:
                queue_post.append(post)
            if chache_pointer:
                queue_edit.append(p)
        return queue_post, queue_edit

async def run():
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(AsyncRemoteHandler(send_to_remote))

    logging.info("Started")

    do = True
    counter = 0
    while do:
        try:
            to_post, to_update = await get_vk_updates()

            if to_post != None and to_update != None:
                if len(to_update) > 0:
                    for post in to_update:
                        await edit_post(post)

                if len(to_post) > 0:
                    for post in to_post:
                        await make_post(post)

                #Чистим кеш каждые 10 записей
                counter+= 1
                if counter % 10 == 0:
                    if fix_cache(cache, 100) and fix_cache(skip_cache, 100):
                        logging.info("[VK] Cache cleared!")
                    if counter > 100_000:
                        counter = 0

            await asyncio.sleep(POLL_DELAY)
        except KeyboardInterrupt:
            bot.close()
            print("Stopping")
            do = False
    
asyncio.run(run())