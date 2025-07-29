import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.redis_service import (
    create_key,
    read_key,
    update_key,
    delete_key,
    list_keys,
    get_ttl
)

router = APIRouter()

class ValueExpire(BaseModel):
    value: dict 
    expire: Optional[int] = None 

import re
from fastapi import HTTPException

@router.post("/keys/{key}")
def create_redis_key(key: str, data: ValueExpire):
    key = key.strip()

    if not re.fullmatch(r"[a-z0-9_-]+", key):
        raise HTTPException(
            status_code=400,
            detail="Invalid key format. Only lowercase letters, digits, underscore (_) and dash (-) are allowed."
        )

    json_value = json.dumps(data.value)

    try:
        result = create_key(key, json_value, expiration=data.expire)
        if result:
            return {"message": f"Key '{key}' successfully saved."}
        else:
            raise HTTPException(status_code=500, detail="Error during creation.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keys/{key}")
def get_redis_key(key: str):
    key = key.strip()
    value = read_key(key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"key '{key}' unfound.")
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
      
        data = value
    return {"key": key, "value": data}

@router.put("/keys/{key}")
def update_redis_key(key: str, data: ValueExpire):
    key = key.strip()
    json_value = json.dumps(data.value)
    expiration = data.expire
    updated = update_key(key, json_value, expiration)
    if updated:
        return {"updated": True, "message": f"key '{key}' updated."}
    raise HTTPException(status_code=404, detail=f"key '{key}' does not exist.")

@router.delete("/keys/{key}")
def delete_redis_key(key: str):
    key = key.strip()
    deleted = delete_key(key)
    if deleted:
        return {"deleted": True, "message": f"key '{key}' deleted."}
    raise HTTPException(status_code=404, detail=f"key '{key}' unfound.")

@router.get("/keys")
def list_all_redis_keys():
    keys = list_keys()
    return {"keys": keys}

@router.get("/keys/{key}/ttl")
def get_redis_key_ttl(key: str):
    key = key.strip()
    ttl = get_ttl(key)
    if ttl == -2:
        raise HTTPException(status_code=404, detail=f"Clé '{key}' does not exist.")
    elif ttl == -1:
        return {"ttl": None, "message": "Key exists but has no expiration."}
    return {"key": key, "ttl": ttl}
