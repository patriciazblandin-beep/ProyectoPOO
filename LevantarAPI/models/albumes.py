from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AlbumOut(BaseModel):
    id_album: Optional[int] = Field(default=None)
    id_artista: int
    titulo: str
    fecha_lanzamiento: Optional[date] = None

    class Config:
        from_attributes = True

class AlbumIn(BaseModel):
    id_artista: int = Field(..., ge=1)
    titulo: str = Field(..., min_length=1, max_length=150)
    fecha_lanzamiento: Optional[date] = None

class AlbumUpdate(BaseModel):
    id_artista: Optional[int] = Field(default=None, ge=1)
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=150)
    fecha_lanzamiento: Optional[date] = None 