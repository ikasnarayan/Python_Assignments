from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas, crud

app = FastAPI(title="Movies API")

# Create tables if not exist
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a movie
@app.post("/movies", response_model=schemas.MovieOut, status_code=201)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_movie(db, movie)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating movie: {e}")

# List movies
@app.get("/movies", response_model=list[schemas.MovieOut])
def list_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        return crud.get_movies(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while fetching movies: {e}")

# Movie actions (get, update, delete)
@app.post("/movies/{movie_id}")
def movie_actions(
    movie_id: int,
    action: str = Query(..., regex="get|update|delete"),
    movie: schemas.MovieUpdate | None = None,
    db: Session = Depends(get_db),
):
    try:
        if action == "get":
            obj = crud.get_movie(db, movie_id)
            if not obj:
                raise HTTPException(status_code=404, detail="Movie not found")
            return obj

        elif action == "update":
            if not movie:
                raise HTTPException(status_code=400, detail="Updated movie data required")
            obj = crud.update_movie(db, movie_id, movie)
            if not obj:
                raise HTTPException(status_code=404, detail="Movie not found")
            return obj

        elif action == "delete":
            ok = crud.delete_movie(db, movie_id)
            if not ok:
                raise HTTPException(status_code=404, detail="Movie not found")
            return {"message": "Movie deleted"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while performing action '{action}': {e}")
