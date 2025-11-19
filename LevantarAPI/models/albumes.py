from pydantic import BaseModel, Field, EmailStr
from typing import Optional
# =========================================================================
# 1. MODELO DE SALIDA (UsuarioOut): Representa un registro COMPLETO de la BD
# ESTA CLASE ES NECESARIA para que routes/usuarios.py pueda hacer la importación.
# =========================================================================
class CancionesOut(BaseModel):
    """Define la estructura completa de la cancion al ser devuelto desde la DB."""
    
    # Campo IDENTITY de la BD
    id_album : Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la tabla music.canciones"
    )

    # Coincide con la columna titulo'
    titulo: str = Field(
        description="Nombre completo de la cancion (NVARCHAR(100) NOT NULL)",
        max_length=100,
        examples=["life goes on"]
    )

    # Campo generado por la BD
    duracion: Optional[time] = Field(
        default=None,
        description="Fecha de registro generada automáticamente ()"
    )

    class Config:
        from_attributes = True

# =========================================================================
# 2. MODELO DE ENTRADA (UsuarioIn): Datos recibidos en POST (Crear)
# Solo requiere 'nombre' y 'email'.
# =========================================================================
class CancionIn(BaseModel):
    """Define la estructura de datos que se espera recibir para crear una cancion."""
    
    titulo: str = Field(
        description="Nombre completo de  la cancion",
        max_length=100
    )
    
    email: EmailStr = Field(
        description="Dirección de correo electrónico única",
        max_length=100
    )


# =========================================================================
# 3. MODELO DE ENTRADA (UsuarioUpdate): Datos recibidos en PUT (Actualizar)
# ESTA CLASE ES NECESARIA para que routes/usuarios.py pueda hacer la importación.
# =========================================================================
class UsuarioUpdate(BaseModel):
    """Define la estructura de datos para actualizar un usuario (todos los campos son opcionales)."""
    
    nombre: Optional[str] = Field(
        default=None,
        description="Nuevo nombre completo del usuario",
        max_length=100
    )
    
    email: Optional[EmailStr] = Field(
        default=None,
        description="Nueva dirección de correo electrónico única",
        max_length=100
    )