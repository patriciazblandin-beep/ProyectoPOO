from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import time

class CancionIn(BaseModel):
    # id  del álbum al que pertenece esta cancion
    id_album: int = Field(..., ge=1)

    # Título de la canción ojo aqui es oblihatorio obligatorio
    titulo: str = Field(..., min_length=1, max_length=150)

    # la uración de la canción es opcional
    duracion: Optional[time] = None

    @field_validator("titulo")
    @classmethod
    def titulo_no_vacio(cls, value):
        if not value.strip():
            raise ValueError("El título de la canción no puwde estar vacío.")
        return value 
class CancionOut(BaseModel):
    id_cancion: Optional[int] = Field(default=None)
    id_album: int
    titulo: str
    duracion: Optional[time] = None

    class Config:
        from_attributes = True  


class CancionUpdate(BaseModel):
    id_album: Optional[int] = Field(default=None, ge=1)
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=150)
    duracion: Optional[time] = None
    