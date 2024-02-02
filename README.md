# Docker Practice: FastAPI and Redis
This project will use docker-compose to create multiple service(container).



### Project structure
```
.
├── Dockerfile
├── README.md
├── app
│   ├── main.py
│   └── requirements.txt
└── docker-compose.yml
```


## Step 1: Create FastAPI service and Redis connection
Firstly, we need to create a basic framework of FastAPI, which can interactive with Redis.
```python
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
```


## Step 2: Prepare dockerfile
Prepare the `Dockerfile` of the FastAPI service.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]
```

## Step 3: Create docker-compose
Combine the multiple service into docker-compose, including the `Dockerfile` we had build in the last step.
```yml
version: '0.0.1'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - redis
  
  redis:
    image: "redis:alpine"
    ports: 
      - "6379:6379"
```

## Step 4: Build docker-compose and run
### a. Create and run the docker-compose
> docker-compose up --build

