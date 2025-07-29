import redis
from app.core.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def create_key(key: str, value: str, expiration: int = None):
   
    return r.set(key, value, ex=expiration)

def read_key(key: str):
    
    return r.get(key)

def update_key(key: str, value: str, expiration: int = None):
    
    if r.exists(key):
        return r.set(key, value, ex=expiration)
    return None

def delete_key(key: str):
  
    
    return r.delete(key)

def list_keys():
   
    return r.keys("*")

def get_ttl(key: str):
   
    return r.ttl(key)

def key_info(key: str):
   
    if not r.exists(key):
        return None
    return {
        "value": r.get(key),
        "ttl": r.ttl(key),
        "type": r.type(key),
        "exists": True,
    }
