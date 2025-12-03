from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# Import your routers
from .routes import users, secure

app = FastAPI()

# Include routers
app.include_router(secure.router)
app.include_router(users.router)

# Step 1: Custom OpenAPI schema with BearerAuth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="JWT Auth Example",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply globally (all endpoints will show lock icon in Swagger UI)
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
