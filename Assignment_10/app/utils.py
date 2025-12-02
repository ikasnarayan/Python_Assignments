from fastapi import HTTPException

def validate_page(page: int):
    if page < 1:
        raise HTTPException(status_code=422, detail="Page must be >= 1")

def compute_total_pages(total_records: int, page_size: int) -> int:
    if total_records == 0:
        return 0
    return (total_records + page_size - 1) // page_size

def build_navigation(page: int, total_pages: int) -> dict:
    previous_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    return {
        "previous_page": previous_page,
        "next_page": next_page,
        "icons": {
            "previous": "⬅️",
            "next": "➡️"
        }
    }
