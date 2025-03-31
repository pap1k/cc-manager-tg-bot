from classes.Storage import CacheDTO

class SkipWallPost(CacheDTO):
    vk_id: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vk_id = kwargs.get("vk_id")