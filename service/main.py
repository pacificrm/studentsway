from fastapi import FastAPI
from service.api.api import main_router
import uvicorn
from service.core.logic.init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    init_db()
    # Yield to indicate the app is ready
    yield


app = FastAPI(project_name="SchoolsWay", lifespan=lifespan)

app.include_router(main_router)

@app.get("/")
async def root():
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
