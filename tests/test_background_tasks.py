import pytest
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.testclient import TestClient


def test_background_tasks_basic():
    app = FastAPI()
    executed_tasks = []

    def task_func(name: str, value: int):
        executed_tasks.append(f"{name}:{value}")

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_func, "test", 123)
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_background_tasks_async_function():
    app = FastAPI()
    executed_tasks = []

    async def async_task(name: str):
        executed_tasks.append(f"async:{name}")

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(async_task, "test_async")
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200


def test_background_tasks_with_kwargs():
    app = FastAPI()
    
    def task_with_kwargs(name: str, value: int = 42):
        pass

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_with_kwargs, "test", value=100)
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200


def test_background_tasks_multiple_tasks():
    app = FastAPI()
    
    def task_one():
        pass
    
    def task_two(arg: str):
        pass

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_one)
        background_tasks.add_task(task_two, "argument")
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200


def test_background_tasks_inheritance():
    tasks = BackgroundTasks()
    
    def simple_task():
        pass
    
    tasks.add_task(simple_task)
    
    assert len(tasks.tasks) == 1


def test_background_tasks_with_complex_args():
    app = FastAPI()
    
    def complex_task(data: dict, items: list, count: int = 1):
        pass

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(
            complex_task,
            {"key": "value"},
            [1, 2, 3],
            count=5
        )
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200


def test_background_tasks_no_args():
    app = FastAPI()
    
    def no_args_task():
        pass

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(no_args_task)
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200


def test_background_tasks_lambda_function():
    app = FastAPI()

    @app.get("/test")
    def test_endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(lambda: None)
        return {"message": "success"}

    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
