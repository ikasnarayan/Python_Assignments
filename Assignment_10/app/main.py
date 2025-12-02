from fastapi import FastAPI
from .routers import movies
from .database import Base, engine

# Create tables on startup (for simple local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie API",
    description="Movies pagination with 10 records per page, exceptions, and Amazon-style navigation icons.",
    version="1.0.0",
)

app.include_router(movies.router, tags=["movies"])
