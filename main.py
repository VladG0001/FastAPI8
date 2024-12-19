from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


app = FastAPI()

movies_db = []

class Movie(BaseModel):
    id: int
    title: str
    director: str
    release_year: int = Field(..., gt=1888)
    rating: float = Field(..., ge=0, le=10)    

    @validator("release_year")
    def check_release_year(cls, v):
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError("Рік випуску не може бути у майбутньому.")
        return v


@app.get("/movies", response_model=List[Movie])
async def get_movies():
    return movies_db


@app.post("/movies", response_model=Movie)
async def create_movie(movie: Movie):
    if any(m.id == movie.id for m in movies_db):
        raise HTTPException(status_code=400, detail="Фільм з таким ID вже існує.")
    movies_db.append(movie)
    return movie


@app.get("/movies/{id}", response_model=Movie)
async def get_movie(id: int):
    movie = next((m for m in movies_db if m.id == id), None)
    if movie is None:
        raise HTTPException(status_code=404, detail="Фільм не знайдено.")
    return movie


@app.delete("/movies/{id}", response_model=dict)
async def delete_movie(id: int):
    global movies_db
    movies_db = [m for m in movies_db if m.id != id]
    return {"message": "Фільм видалено."}
