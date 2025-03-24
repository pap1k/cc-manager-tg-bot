import datetime
from classes.Storage import CacheDTO

class PostCache(CacheDTO):
    vk_id: int
    tg_id: int
    post_time: datetime.datetime
    last_edit: datetime.datetime

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.vk_id = kwargs.get("vk_id")
        self.tg_id = kwargs.get("tg_id")
        self.post_time = kwargs.get("post_time")

        if self.post_time != None:
            self.post_time = datetime.datetime.fromtimestamp(self.post_time)

        self.last_edit = kwargs.get("last_edit")
        if self.last_edit != None:
            self.last_edit = datetime.datetime.fromtimestamp(self.last_edit)