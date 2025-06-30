from cache import redis_client
import json

redis_client.set("testkey", json.dumps([0,1,2,3]))

r = redis_client.get("testkey1")
if r:
    r = json.loads(r)
    print(type(r), r)