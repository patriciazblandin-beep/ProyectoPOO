from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =========================================================================
# 1. MODELO DE ENTRADA (PlaylistIn): Datos recibidos en POST (Crear)
# =========================================================================
class PlaylistIn(BaseModel):
    """Define la estructura de datos para crear una nueva playlist."""
    nombre: str
    id_usuario: int # Clave foránea al modelo de Usuarios
    descripcion: Optional[str] = None

# =========================================================================
# 2. MODELO DE SALIDA (PlaylistOut): Datos que se devuelven al cliente
# =========================================================================
class PlaylistOut(BaseModel):
    """Define la estructura de datos completa que se devuelve al obtener una playlist."""
    id_playlists: int
    nombre: str
    id_usuario: int
    descripcion: Optional[str] = None
    fecha_creacion: datetime # Se asume que la base de datos devuelve un timestamp o datetime

# =========================================================================
# 3. MODELO DE ACTUALIZACIÓN (PlaylistUpdate): Campos opcionales para PUT
# =========================================================================
class PlaylistUpdate(BaseModel):
    """Define los campos opcionales que pueden ser actualizados."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    
    # Configuramos Pydantic para permitir el uso de índices
    class Config:
        from_attributes = True