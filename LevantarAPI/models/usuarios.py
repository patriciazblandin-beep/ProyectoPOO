from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# =========================================================================
# 1. MODELO DE SALIDA (UsuarioOut): Representa un registro COMPLETO de la BD
# ESTA CLASE ES NECESARIA para que routes/usuarios.py pueda hacer la importación.
# =========================================================================
class UsuarioOut(BaseModel):
    """Define la estructura completa del usuario al ser devuelto desde la DB."""
    
    # Campo IDENTITY de la BD
    id_usuario: Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la tabla music.usuarios"
    )

    # Coincide con la columna 'nombre'
    nombre: str = Field(
        description="Nombre completo del usuario (NVARCHAR(100) NOT NULL)",
        max_length=100,
        examples=["Patricio Zelaya"]
    )

    # Coincide con la columna 'email' y usa validación EmailStr de Pydantic
    email: EmailStr = Field(
        description="Dirección de correo electrónico única (NVARCHAR(100) UNIQUE NOT NULL)",
        max_length=100,
        examples=["patricio.zelaya@example.com"]
    )
    
    # Campo generado por la BD
    fecha_registro: Optional[datetime] = Field(
        default=None,
        description="Fecha de registro generada automáticamente (DATETIME DEFAULT SYSDATETIME())"
    )

    class Config:
        from_attributes = True

# =========================================================================
# 2. MODELO DE ENTRADA (UsuarioIn): Datos recibidos en POST (Crear)
# Solo requiere 'nombre' y 'email'.
# =========================================================================
class UsuarioIn(BaseModel):
    """Define la estructura de datos que se espera recibir para crear un usuario."""
    
    nombre: str = Field(
        description="Nombre completo del usuario",
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