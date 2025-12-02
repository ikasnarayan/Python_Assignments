from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Movies API with Exception Handling")

class Movie(BaseModel):
    id: int
    title: str
    director: str

movies_db = {}

# Create a movie
@app.post("/movies/")
def create_movie(movie: Movie):
    try:
        if movie.id in movies_db:
            raise HTTPException(status_code=400, detail="Movie already exists")
        movies_db[movie.id] = movie
        return movie
    except HTTPException as he:
        # Re-raise known HTTP errors
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating movie: {e}")

# Get all movies
@app.get("/movies/")
def get_movies():
    try:
        return list(movies_db.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while fetching movies: {e}")

# Perform actions on a movie
@app.post("/movies/{movie_id}")
def movie_actions(
    movie_id: int,
    action: str = Query(..., regex="get|update|delete"),
    updated: Movie = None
):
    try:
        if action == "get":
            movie = movies_db.get(movie_id)
            if not movie:
                raise HTTPException(status_code=404, detail="Movie not found")
            return movie

        elif action == "update":
            if movie_id not in movies_db:
                raise HTTPException(status_code=404, detail="Movie not found")
            if not updated:
                raise HTTPException(status_code=400, detail="Updated movie data required")
            movies_db[movie_id] = updated
            return updated

        elif action == "delete":
            if movie_id not in movies_db:
                raise HTTPException(status_code=404, detail="Movie not found")
            del movies_db[movie_id]
            return {"message": "Movie deleted"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while performing action '{action}': {e}")
