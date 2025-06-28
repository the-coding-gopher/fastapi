import logging
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.requestlogging import RequestLoggingMiddleware, add_request_logging_middleware
from fastapi.middleware.settings import RequestLoggingSettings


def test_request_logging_middleware_basic():
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    app.add_middleware(RequestLoggingMiddleware)
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.json() == {"message": "test"}


def test_request_logging_middleware_with_custom_logger(caplog):
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    app.add_middleware(
        RequestLoggingMiddleware,
        logger_name="test.logger",
        log_level=logging.INFO
    )
    
    client = TestClient(app)
    
    with caplog.at_level(logging.INFO, logger="test.logger"):
        response = client.get("/test")
    
    assert response.status_code == 200
    assert len(caplog.records) == 1
    assert "GET /test - 200" in caplog.records[0].message
    assert "s" in caplog.records[0].message


def test_request_logging_middleware_disabled():
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    app.add_middleware(
        RequestLoggingMiddleware,
        enabled=False
    )
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.json() == {"message": "test"}


def test_request_logging_settings():
    settings = RequestLoggingSettings()
    assert settings.request_logging_enabled is True
    assert settings.request_logging_logger_name == "fastapi.requests"
    assert settings.request_logging_level == logging.INFO


def test_add_request_logging_middleware_convenience_function(caplog):
    app = FastAPI()
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    add_request_logging_middleware(app)
    
    client = TestClient(app)
    
    with caplog.at_level(logging.INFO, logger="fastapi.requests"):
        response = client.get("/test")
    
    assert response.status_code == 200
    assert len(caplog.records) == 1
    assert "GET /test - 200" in caplog.records[0].message


def test_request_logging_middleware_different_methods(caplog):
    app = FastAPI()
    
    @app.get("/test")
    async def get_endpoint():
        return {"method": "GET"}
    
    @app.post("/test")
    async def post_endpoint():
        return {"method": "POST"}
    
    app.add_middleware(
        RequestLoggingMiddleware,
        logger_name="test.methods",
        log_level=logging.INFO
    )
    
    client = TestClient(app)
    
    with caplog.at_level(logging.INFO, logger="test.methods"):
        get_response = client.get("/test")
        post_response = client.post("/test")
    
    assert get_response.status_code == 200
    assert post_response.status_code == 200
    assert len(caplog.records) == 2
    assert "GET /test - 200" in caplog.records[0].message
    assert "POST /test - 200" in caplog.records[1].message


def test_request_logging_middleware_with_error_status(caplog):
    app = FastAPI()
    
    @app.get("/error")
    async def error_endpoint():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    
    app.add_middleware(
        RequestLoggingMiddleware,
        logger_name="test.errors",
        log_level=logging.INFO
    )
    
    client = TestClient(app)
    
    with caplog.at_level(logging.INFO, logger="test.errors"):
        response = client.get("/error")
    
    assert response.status_code == 404
    assert len(caplog.records) == 1
    assert "GET /error - 404" in caplog.records[0].message
