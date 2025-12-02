from fastapi import FastAPI
from . import models, database
from .routes import users, secure

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FastAPI Auth Example")

app.include_router(users.router)
app.include_router(secure.router)
