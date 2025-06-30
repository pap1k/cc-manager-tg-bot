import asyncio, datetime, logging, json
from typing import Tuple
from classes.CacheModels.PostCache import PostCache
from config import settings
from cache import redis_client
from classes.bot import bot
from classes.vk import VK
from classes.VkClasses import Wall
from helpers.vk_to_tg import vk_to_tg
from helpers.send_log import AsyncRemoteHandler, send_to_remote

POLL_DELAY = 60

CACHE_ALIVE = 60*60*48 # 2 days
_KEY_SKIP = "SkipWallDataKey:"
_KEY_POSTED = "PostedKey:"

vk = VK(settings.VK_TOKEN)

start_time = datetime.datetime.now()

async def make_post(post: Wall):
    tg = await vk_to_tg(post)
    if not tg:
        redis_client.setex(_KEY_SKIP+str(post.id), CACHE_ALIVE, post.id)
        return

    if tg.topic_id == -1:
        logging.info(f"[VK] Функция преобразования не определила тег, пропускаем")
        c = PostCache(vk_id=post.id, tg_id=0, post_time=post.date, last_edit=post.edited)
    else:
        logging.info(f"[VK] Выкладываем пост <{post.id}> в чат <{tg.chat_id}>, топик <{tg.topic_id}>")
        # TODO чето придумать с отправкой нескольких фото, а надо оно вообще или нет - хз
        if not settings.IS_TEST:
            if len(tg.attachments) > 0:
                resp = await bot.send_photo(tg.chat_id, tg.attachments[0], tg.text, message_thread_id = tg.topic_id)
            else:            
                resp = await bot.send_message(tg.chat_id, tg.text, message_thread_id = tg.topic_id, parse_mode="HTML", disable_web_page_preview=True)
            c = PostCache(vk_id=post.id, tg_id=resp.message_id, topic_id=resp.message_thread_id, post_time=post.date, last_edit=post.edited)
        else:
            logging.debug("POST CALLED")

    redis_client.setex(_KEY_POSTED+str(post.id), CACHE_ALIVE, c.to_json())

async def edit_post(post: PostCache):
    logging.info(f"[EDIT] Editing post id {post.vk_id} with tg_id = {post.tg_id}")
    post.last_edit = datetime.datetime.now()
    redis_client.setex(_KEY_POSTED + str(post.vk_id), CACHE_ALIVE, post.to_json())
    if not settings.IS_TEST:
        return #TODO
    else:
        logging.debug("EDIT CALLED")

async def get_vk_updates() -> Tuple[list[Wall], list[PostCache]]:
    wall = await vk.wall_get(domain=settings.VK_GROUP_DOMAIN, count=10)
    if wall:
        wall.reverse()

        queue_post = []
        queue_edit = []

        for post in wall:
            if post.date < start_time:
                continue
            # Проверка новых постов
            need_post = True
            cache_pointer = None
            
            skip_cache = redis_client.get(_KEY_SKIP + str(post.id))
            if skip_cache:
                need_post = False

            cached_post = redis_client.get(_KEY_POSTED + str(post.id))
            if cached_post:
                need_post = False
                if post.edited:
                    cached_post: PostCache = PostCache.from_json(json.loads(cached_post))
                    if cached_post.last_edit > post.edited:
                        cache_pointer = cached_post

            if need_post:
                queue_post.append(post)
            if cache_pointer:
                queue_edit.append(cache_pointer)
        return queue_post, queue_edit

async def run():
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(AsyncRemoteHandler(send_to_remote))

    logging.info("Started")

    do = True
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

            await asyncio.sleep(POLL_DELAY)
        except KeyboardInterrupt:
            bot.close()
            print("Stopping")
            do = False
    
asyncio.run(run())