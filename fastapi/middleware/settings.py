import logging
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class RequestLoggingSettings(BaseSettings):
    model_config = ConfigDict(env_prefix="FASTAPI_")
    
    request_logging_enabled: bool = True
    request_logging_logger_name: str = "fastapi.requests"
    request_logging_level: int = logging.INFO
