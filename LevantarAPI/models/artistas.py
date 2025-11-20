from pydantic import BaseModel, Field, field_validator

from typing import Optional

class ArtistaOut(BaseModel):
    id_artista: Optional[int] = Field(default=None)
    nombre: str
    discografica: Optional[str] = None

    class Config:
        from_attributes = True

class ArtistaIn(BaseModel):
    nombre: str = Field(..., max_length=100)
    discografica: Optional[str] = Field(default=None, max_length=150)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value):
        if not value or not value.strip():
            raise ValueError("El nombre del artista no puede estar vacío.")
        return value



class ArtistaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    discografica: Optional[str] = Field(default=None, max_length=150)
 