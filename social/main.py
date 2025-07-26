import logging
from contextlib import asynccontextmanager

from database import database
from logging_conf import configure_logging
from routers.posts import router as post_router
from routers.users import router as user_router

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()

origins = [
    "http://localhost:3000"
]

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = [
        "PUT", "PATCH", "DELETE", "POST", "GET"
    ]
)


app.include_router(post_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)


if __name__ == "__main__":
    import uvicorn   #noqa: E402

    uvicorn.run("main:app", host="localhost", port=8443, log_level="debug", reload=True)
