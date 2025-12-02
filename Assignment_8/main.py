from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Movie API", description="Manage movies with FastAPI + Swagger")

# Movie schema
class Movie(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genre: str

# In-memory DB
movies_db: List[Movie] = []

@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db

@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    movies_db.append(movie)
    return movie

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")
    
