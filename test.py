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

cache = CacheStorage("test", TestData, True)

elist = []
elist.append(TestData(f1="teststr1", f2=123312))
elist.append(TestData(f1="teststr2", f2=3214))
elist.append(TestData(f1="teststr3", f2=1241))

cache.store(elist)

fromcache: TestData = cache.get()
print(fromcache[2].f1)