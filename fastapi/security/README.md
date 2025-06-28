# FastAPI Security

This module provides security utilities and authentication implementations for FastAPI applications.

## Overview

FastAPI's security module offers a comprehensive set of tools for implementing authentication and authorization in your APIs. It supports various authentication schemes including OAuth2, API keys, HTTP Basic/Bearer authentication, and more.

## Security Components

### `oauth2.py`
OAuth2 authentication flows including Authorization Code, Client Credentials, and Password flows.

```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user and return token
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

### `api_key.py`
API key authentication for header, query parameter, or cookie-based authentication.

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/protected")
async def protected_route(api_key: str = Depends(api_key_header)):
    return {"message": "Access granted"}
```

### `http.py`
HTTP authentication schemes including Basic and Bearer authentication.

```python
from fastapi.security import HTTPBasic, HTTPBearer

security_basic = HTTPBasic()
security_bearer = HTTPBearer()

@app.get("/basic")
async def basic_auth(credentials: HTTPBasicCredentials = Depends(security_basic)):
    return {"username": credentials.username}
```

### `open_id_connect_url.py`
OpenID Connect authentication support for integration with identity providers.

```python
from fastapi.security import OpenIdConnect

openid_connect = OpenIdConnect(openIdConnectUrl="/.well-known/openid_configuration")
```

### `base.py`
Base classes and utilities for implementing custom security schemes.

### `utils.py`
Utility functions for security operations including token validation, password hashing, and security scheme helpers.

## Common Patterns

### JWT Token Authentication
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

def verify_token(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### Role-Based Access Control
```python
def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

@app.get("/admin")
async def admin_only(user: dict = Depends(require_role("admin"))):
    return {"message": "Admin access granted"}
```

## Security Best Practices

- Always use HTTPS in production
- Implement proper token expiration and refresh mechanisms
- Use strong, randomly generated secrets for signing tokens
- Validate and sanitize all input data
- Implement rate limiting to prevent abuse
- Log security events for monitoring

## Learn More

For detailed tutorials and advanced security patterns, see the [FastAPI Security documentation](https://fastapi.tiangolo.com/tutorial/security/).
