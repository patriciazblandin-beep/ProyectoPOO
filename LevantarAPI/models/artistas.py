from pydantic import BaseModel
from typing import Optional

# =========================================================================
# 1. MODELO DE ENTRADA (artistaIn): Datos recibidos en POST (Crear)
# =========================================================================
class ArtistaIn(BaseModel):
    """Define la estructura de datos para crear una nueva playlist."""
    nombre: str
    discografica: str 

# =========================================================================
# 2. MODELO DE SALIDA (artistatOut): Datos que se devuelven al cliente
# =========================================================================
class ArtistaOut(BaseModel):
    """Define la estructura de datos completa que se devuelve al obtener un Artista."""
    id_artista: int
    nombre: str
    discografica: str


# =========================================================================
# 3. MODELO DE ACTUALIZACIÓN (artista): Campos opcionales para PUT
# =========================================================================
class ArtistaUpdate(BaseModel):
    """Define los campos opcionales que pueden ser actualizados."""
    nombre: Optional[str] = None
    discografica: Optional[str] = None
    
    # Configuramos Pydantic para permitir el uso de índices
    class Config:
        from_attributes = True 