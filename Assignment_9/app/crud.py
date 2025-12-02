from sqlalchemy.orm import Session
from . import models, schemas

def get_movie(db: Session, movie_id: int) -> models.Movie | None:
    return db.get(models.Movie, movie_id)

def get_movies(db: Session, skip: int = 0, limit: int = 50) -> list[models.Movie]:
    return db.query(models.Movie).offset(skip).limit(limit).all()

def create_movie(db: Session, m: schemas.MovieCreate) -> models.Movie:
    obj = models.Movie(title=m.title, director=m.director, year=m.year)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_movie(db: Session, movie_id: int, m: schemas.MovieUpdate) -> models.Movie | None:
    obj = get_movie(db, movie_id)
    if not obj:
        return None
    if m.title is not None:
        obj.title = m.title
    if m.director is not None:
        obj.director = m.director
    if m.year is not None:
        obj.year = m.year
    db.commit()
    db.refresh(obj)
    return obj

def delete_movie(db: Session, movie_id: int) -> bool:
    obj = get_movie(db, movie_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
