from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import SessionLocal
from ..crud import get_movies_page, count_movies
from ..utils import validate_page, compute_total_pages, build_navigation
from ..schemas import PaginatedMoviesResponse, MovieOut

router = APIRouter()

PAGE_SIZE = 10  # Fixed page size as requested

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/movies/", response_model=PaginatedMoviesResponse)
def list_movies(
    page: int = Query(1, ge=1, description="Page number, starts at 1"),
    year: Optional[int] = Query(None, description="Optional filter by year"),
    genre: Optional[str] = Query(None, description="Optional filter by genre"),
    db: Session = Depends(get_db)
):
    try:
        validate_page(page)

        total_records = count_movies(db, year=year, genre=genre)
        total_pages = compute_total_pages(total_records, PAGE_SIZE)

        # If there are records but page exceeds total_pages, return 404
        if total_records > 0 and page > total_pages:
            raise HTTPException(status_code=404, detail="Page not found")

        # If no records, return empty set consistently
        movies = get_movies_page(db, page=page, page_size=PAGE_SIZE, year=year, genre=genre)

        return {
    "page": page,
    "page_size": PAGE_SIZE,
    "total_records": total_records,
    "total_pages": total_pages,
    "movies": [MovieOut.model_validate(m, from_attributes=True) for m in movies],
    "navigation": build_navigation(page, total_pages)
}

    except HTTPException:
        # Allow explicit HTTP exceptions to bubble as-is
        raise
    except Exception as e:
        # Unexpected server-side error
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
