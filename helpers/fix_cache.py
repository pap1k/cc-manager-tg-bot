from classes.Storage import CacheDTO, CacheStorage


def fix_cache(storage: CacheStorage, max_size: int = 100):
    if storage.is_list:
        cache = storage.get()
        if len(cache) > max_size:
            cache = cache[-max_size]
            storage.store(cache)
            return True
    return False
