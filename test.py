from classes.Storage import CacheStorage, CacheDTO

class TestData(CacheDTO):
    f1: str
    f2: int
    def __init__(self, **data):
        self.f1 = data.get("f1")
        self.f2 = data.get("f2")
        super().__init__(**data)

class TestDataList(CacheDTO):
    f1: str
    f2: int
    def __init__(self, **data):
        self.f1 = data.get("f1")
        self.f2 = data.get("f2")
        super().__init__(**data)

cache = CacheStorage("test", TestData)

elem = TestData(f1="teststr", f2=123312)

cache.store(elem)

fromcache: TestData = cache.get()
print(fromcache.f2)