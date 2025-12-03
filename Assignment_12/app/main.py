from fastapi import FastAPI
from app.routes import file_routes

app = FastAPI(title="FastAPI Threading Example")

# Include routes
app.include_router(file_routes.router)
