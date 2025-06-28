# FastAPI OpenAPI

This module handles OpenAPI schema generation and documentation for FastAPI applications.

## Overview

FastAPI automatically generates OpenAPI schemas for your API, which power the interactive documentation (Swagger UI and ReDoc). This module contains the core functionality for schema generation, customization, and documentation rendering.

## Module Contents

### `constants.py`
Contains constants used throughout the OpenAPI schema generation process, including HTTP status codes, content types, and schema definitions.

### `docs.py`
Handles the generation and serving of interactive API documentation (Swagger UI and ReDoc interfaces).

### `models.py`
Pydantic models that represent OpenAPI schema components, including operations, parameters, responses, and security definitions.

### `utils.py`
Utility functions for schema generation, including parameter extraction, response modeling, and schema merging.

## Basic Customization

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A custom API with OpenAPI documentation",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "items",
            "description": "Operations with items",
        }
    ]
)

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"item_id": "Foo"}]
```

## Advanced Schema Customization

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

## Key Features

- **Automatic Schema Generation**: Schemas are generated from your Python type hints
- **Interactive Documentation**: Swagger UI and ReDoc interfaces are automatically available
- **Customizable**: Full control over OpenAPI schema generation and documentation
- **Standards Compliant**: Generates valid OpenAPI 3.0+ schemas
- **Security Integration**: Automatic security scheme documentation

## Learn More

For comprehensive guides on customizing OpenAPI schemas and documentation, see the [FastAPI OpenAPI documentation](https://fastapi.tiangolo.com/advanced/extending-openapi/).
