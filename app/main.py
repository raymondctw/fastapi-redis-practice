from fastapi import FastAPI, HTTPException
from redis import StrictRedis
import uvicorn

app = FastAPI()
redis = StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@app.get("/get-all")
async def get_all_keys_values():
    keys = redis.keys("*")
    key_value_pairs = {key: redis.get(key) for key in keys}
    return {"keys_values": key_value_pairs}

@app.post("/set/{key}/{value}")
async def set_key_value(key: str, value: str):
    redis.set(key, value)
    return {"message": f"Key '{key}' set with value '{value}'"}

@app.get("/get/{key}")
async def get_value(key: str):
    value = redis.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found")
    return {"key": key, "value": value}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)