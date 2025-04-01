from fastapi import FastAPI
from router.posts import router as post_router

app = FastAPI()
app.include_router(post_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8443, log_level="info")
