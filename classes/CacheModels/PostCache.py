import datetime, json

class PostCache:
    vk_id: int
    tg_id: int
    topic_id: int
    post_time: datetime.datetime
    last_edit: datetime.datetime

    def __init__(self, **kwargs):
        self.vk_id = kwargs.get("vk_id")
        self.tg_id = kwargs.get("tg_id")
        self.topic_id = kwargs.get("topic_id")
        self.post_time = kwargs.get("post_time")
        if self.post_time != None:
            if type(self.post_time) == int or type(self.post_time) == float:
                self.post_time = datetime.datetime.fromtimestamp(self.post_time)

        self.last_edit = kwargs.get("last_edit")
        if self.last_edit != None:
            if type(self.last_edit) == int or type(self.last_edit) == float:
                self.last_edit = datetime.datetime.fromtimestamp(self.last_edit)
        else:
            self.last_edit = self.post_time

    def from_json(self, **kwargs) -> 'PostCache':
        return self(**kwargs)

    def to_json(self) -> str:
        tojson = {
            "vk_id": self.vk_id,
            "tg_id": self.tg_id,
            "topic_id": self.topic_id,
            "post_time": self.post_time.timestamp(),
            "last_edit": self.last_edit.timestamp()
        }
        return json.dumps(tojson)