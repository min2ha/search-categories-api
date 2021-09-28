from typing import Optional
from fastapi import FastAPI
import uvicorn

api = FastAPI()


@api.get("/")
def read_root():
    return {"Hello": "Search Categories API"}


@api.get("/categories/{category_id}")
def read_category(category_id: int, q: Optional[str] = None):
    return {"category_id": category_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="0.0.0.0")
