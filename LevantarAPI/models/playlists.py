
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlaylistOut(BaseModel):
    id_playlists: Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la tabla music.playlists"
    )
    id_usuario: int = Field(
        description="ID del usuario que creó la playlist (INT NOT NULL)"
    )
    nombre: str = Field(
        description="Nombre de la playlist (NVARCHAR(200) NOT NULL)",
        max_length=200
    )
    fecha_creacion: Optional[datetime] = Field(
        default=None,
        description="Fecha de creación generada automáticamente (DATETIME DEFAULT SYSDATETIME())"
    )

    class Config:
        from_attributes = True

class PlaylistIn(BaseModel):
    id_usuario: int = Field(description="ID del usuario que crea la playlist")
    nombre: str = Field(description="Nombre de la playlist", max_length=200)

class PlaylistUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, description="Nuevo nombre de la playlist", max_length=200)