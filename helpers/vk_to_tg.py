from classes.VkClasses import Wall, Attachment
from config import settings
import logging

class TgPost:
    text: str
    chat_id: int
    topic_id: int
    attachments: list[str]

    def __init__(self, text: str, chat_id: int, topic_id: int):
        self.text = text
        self.chat_id = chat_id
        self.topic_id = topic_id
        self.attachments = []

    def add_attach(self, attach: Attachment):
        self.attachments.append(attach.photo.orig_photo.url)

topics = {
    "forum": 6,
    "admin": 58,
}

tags = {
    "ccnews": "forum",
    "ccbannews": "admin",
    "ccother": "__skip",
    "ccgroup": "__skip",
    "cclottery": "__skip",
    "ccevents": "__skip",
    "ccproject": "__skip",
}

def extract_tag_and_text(content: str) -> tuple[str | None, str]:
    lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
    
    tag = None
    if lines and lines[0].startswith('#'):
        tag = lines[0].strip('#').strip()
    
    if len(lines) > 1:
        lines[1] += "\n"
        text = '\n'.join(lines[1:])
    else:
        text = ""


    return tag if tag else None, text.strip()

def vk_to_tg(wall: Wall) -> TgPost | None:
    posttag, posttext = extract_tag_and_text(wall.text)
    topic = -1
    if posttag:
        for tag in tags:
            if tag == posttag:
                topicname = tags[tag]
                if topicname == "__skip":
                    logging.info(f"[PARSE] Пропускаем пост <{wall.id}>, тег <{posttag}>")
                    return None
                if topicname in topics:
                    topic = topics[topicname]
                else:
                    logging.warning(f"[PARSE] Не получилось найти топик для тега <{posttag}>")
        if topic == -1:
            logging.warning(f"[PARSE] Обнаружен неизвестный тег: <{posttag}>")
    else:
        logging.warning(f"[PARSE] Не получилось найти тег у поста {wall.id}")

    post = TgPost(posttext, settings.TG_CHAT_ID, topic)
    # Скрыл аттачи чтобы можно было нормально постить длинный текст (лимиты тг)
    # if len(wall.attachments) > 0:
    #     for attach in wall.attachments:
    #         if attach.photo:
    #             post.add_attach(attach)
    
    if len(post.attachments) == 0:
        if wall.copyright:
            link_txt = "абоба"
            match wall.copyright.name:
                case "gta-trinity.com":
                    link_txt = "Посмотреть на форуме"
            post.text += f"\n\n<a href=\"{wall.copyright.link}\">{link_txt}</a>"
        
        post.text += f"\n<a href=\"https://vk.com/offtrinityrpg?w=wall-145098987_{wall.id}\">Пост в ВК</a>"

    return post

