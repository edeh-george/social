from contextlib import asynccontextmanager

from database import database
from router.posts import router as post_router

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8443, log_level="info", reload=True)
