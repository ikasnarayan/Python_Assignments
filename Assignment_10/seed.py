# Run: python seed.py
from app.database import SessionLocal, Base, engine
from app.models import Movie

Base.metadata.create_all(bind=engine)

sample_movies = [
    {"title": f"Movie {i}", "year": 2000 + (i % 25), "genre": ["Action", "Drama", "Sci-Fi", "Comedy"][i % 4]}
    for i in range(1, 101)  # 100 movies
]

def run():
    db = SessionLocal()
    try:
        # Clear existing for repeatable seeds (optional: comment out in prod)
        db.query(Movie).delete()
        db.commit()

        for i, m in enumerate(sample_movies, start=1):
            db.add(Movie(id=i, title=m["title"], year=m["year"], genre=m["genre"]))
        db.commit()
        print("Seeded 100 movies.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
