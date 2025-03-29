from abc import abstractmethod
from typing import Literal
import json
import os

class CacheDTO:
    data : object
    def __init__(self, **data):
        self.data = data

    def __repl__(self):
        return json.dumps(self.data)

    @abstractmethod
    def to_json(self):
        return json.dumps(self.data)

    @abstractmethod
    def from_json(self):
        return json.loads(self.data)

class Storage:

    method: Literal["cache", "database"]

    def __init__(self, method: Literal["cache", "database"]):
        self.method = method

    @abstractmethod
    def store(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> object:
        pass
        

class CacheStorage(Storage):

    file: str
    classbind: CacheDTO
    is_list: bool

    def __init__(self, key:str, classbind: CacheDTO | None, is_list = False):
        super().__init__("cache")
        self.file = key
        self.classbind = classbind
        self.is_list = is_list

    def store(self, data: object | CacheDTO):
        towrite = ""
        if isinstance(data, CacheDTO):
            towrite = data.to_json()
        elif isinstance(data, list) and all(isinstance(elem, CacheDTO) for elem in data):
            objs = []
            for e in data:
                objs.append(e.to_json())
            towrite = f"[{','.join(objs)}]"
        else:
            towrite = json.dumps(data)
        with open(f"cache/{self.file}.json", 'w', encoding='utf-8') as f:
            f.write(towrite)
        return True
    
    # Если не установлено класса сериализации, то возвращаем голый объект
    # Если класс установлен, проверяем, установлен ли флаг что он лист
    # Если да, то возвращаем массив этих объектов
    # НЕ ПОДДЕРЖИВАЕТ МАССИВ МАССИВОВ
    def get(self) -> CacheDTO | object:
        if not os.path.isfile(f"cache/{self.file}.json"):
            with open(f"cache/{self.file}.json", 'w', encoding='utf-8') as f:
                f.close()
        with open(f"cache/{self.file}.json", 'r', encoding='utf-8') as f:
            txt = f.read()
            if txt == '':
                if self.is_list: return []
                else: return {}
            data = json.loads(txt)
            if self.classbind != None:
                if self.is_list:
                    r = []
                    for e in data:
                        r.append(self.classbind(**e))
                    return r
                else:
                    return self.classbind(**data)
            else:
                return data
        return None
    
class DataBaseStorage(Storage):
    
    model: object

    def __init__(self, model: object):
        super().__init__("database")

    def store():
        pass

    def get():
        pass

