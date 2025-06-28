# FastAPI Middleware

This module provides middleware components for FastAPI applications, built on top of Starlette's middleware system.

## Overview

Middleware in FastAPI allows you to add functionality that runs before and after each request. This module includes commonly used middleware for CORS, compression, security, and more.

## Available Middleware

### `cors.py`
Cross-Origin Resource Sharing (CORS) middleware for handling cross-origin requests.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### `gzip.py`
GZip compression middleware to automatically compress responses.

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### `httpsredirect.py`
HTTPS redirect middleware to automatically redirect HTTP requests to HTTPS.

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

### `trustedhost.py`
Trusted host middleware to validate the Host header against a list of allowed hosts.

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["example.com", "*.example.com"]
)
```

### `wsgi.py`
WSGI middleware for mounting WSGI applications within FastAPI.

```python
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask

flask_app = Flask(__name__)
app.mount("/flask", WSGIMiddleware(flask_app))
```

## Usage Pattern

All middleware follows the same pattern:

```python
from fastapi import FastAPI
from fastapi.middleware.{middleware_name} import {MiddlewareClass}

app = FastAPI()
app.add_middleware(MiddlewareClass, **options)
```

## Learn More

For detailed configuration options and advanced usage, see the [FastAPI Middleware documentation](https://fastapi.tiangolo.com/tutorial/middleware/) and [Starlette Middleware documentation](https://www.starlette.io/middleware/).
