import logging
from fastapi import FastAPI
from fastapi.middleware.requestlogging import add_request_logging_middleware
from fastapi.middleware.settings import RequestLoggingSettings

logging.basicConfig(level=logging.INFO)

app = FastAPI()

add_request_logging_middleware(app)

settings = RequestLoggingSettings(
    request_logging_enabled=True,
    request_logging_logger_name="my_app.requests",
    request_logging_level=logging.DEBUG
)
add_request_logging_middleware(app, settings=settings)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
