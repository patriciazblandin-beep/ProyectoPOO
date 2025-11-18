import json
import logging
from typing import List, Optional

from fastapi import HTTPException, status
# ------------------------------------------------------------------
# IMPORTACIÓN CORRECTA
from models.usuarios import UsuarioOut, UsuarioIn, UsuarioUpdate 
# ------------------------------------------------------------------
from utils.database import execute_query_json # Función asumida

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Función Auxiliar para Mapeo (ID) ---
async def _fetch_usuario_by_id(id_usuario: int) -> Optional[UsuarioOut]:
    """Busca un usuario por ID."""
    sqlfind: str = """
        SELECT [id_usuario], [nombre], [email], [fecha_registro]
        FROM [music].[usuarios]
        WHERE id_usuario = ?;
    """
    params = [id_usuario]
    
    result = await execute_query_json(sqlfind, params=params, fetch_one=True)

    if result:
        return UsuarioOut(**result)
    return None

# --- Función Auxiliar para Mapeo (Email) ---
async def _fetch_usuario_by_email(email: str) -> Optional[UsuarioOut]:
    """Busca un usuario por email después de la inserción o actualización."""
    sqlfind: str = """
        SELECT [id_usuario], [nombre], [email], [fecha_registro]
        FROM [music].[usuarios]
        WHERE email = ?;
    """
    params = [email]
    
    result = await execute_query_json(sqlfind, params=params, fetch_one=True)
    
    if result:
        return UsuarioOut(**result)
    return None

# --- CREATE (POST) ---
async def create_user(usuario_data: UsuarioIn) -> UsuarioOut:
    """Inserta un nuevo usuario y devuelve el objeto completo."""
    
    sqlscript: str = """
        INSERT INTO [music].[usuarios] ([nombre], [email])
        VALUES (?, ?);
    """
    
    params = [usuario_data.nombre, usuario_data.email]

    try:
        # 1. Ejecutar INSERT.
        await execute_query_json(sqlscript, params=params, needs_commit=True)
        
        # 2. Buscar el registro insertado (usando el campo UNIQUE 'email')
        usuario_creado = await _fetch_usuario_by_email(usuario_data.email)
        
        if usuario_creado:
            return usuario_creado
        else:
            raise HTTPException(status_code=500, detail="Error desconocido: Usuario creado pero no se pudo recuperar.")
            
    except HTTPException:
        # Si la excepción ya es HTTPException (ej. 404 de get_one_u), la propagamos
        raise 
    except Exception as e:
        # Manejo de error de UNIQUE constraint (email duplicado)
        # CORRECCIÓN CLAVE: Convertir el código de estado a string para usar 'in'
        if str(status.HTTP_409_CONFLICT) in str(e): 
            raise HTTPException(status_code=409, detail=f"El email '{usuario_data.email}' ya está registrado.")
        
        # Manejo de otros errores de base de datos
        raise HTTPException(status_code=500, detail=f"Error en la base de datos al crear usuario: { str(e) }")

# --- READ ALL (GET /) ---
async def get_all_u() -> List[UsuarioOut]:
    """Obtiene una lista de todos los usuarios."""
    
    selectscript = """
        SELECT [id_usuario], [nombre], [email], [fecha_registro]
        FROM [music].[usuarios];
    """

    try:
        # Usamos fetch_all=True
        results = await execute_query_json(selectscript, fetch_all=True)
        
        # Mapea la lista de diccionarios a una lista de modelos UsuarioOut
        return [UsuarioOut(**data) for data in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos al listar usuarios: { str(e) }")

# --- READ ONE (GET /{id}) ---
async def get_one_u(id_usuario: int) -> UsuarioOut:
    """Obtiene un usuario por su ID."""
    
    usuario = await _fetch_usuario_by_id(id_usuario)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con ID {id_usuario} no encontrado.")
    
    return usuario

# --- UPDATE (PUT /{id}) ---
async def update_user(id_usuario: int, usuario_data: UsuarioUpdate) -> UsuarioOut:
    """Actualiza la información de un usuario y retorna el objeto actualizado."""

    # Preparamos los campos a actualizar
    updates = []
    params = []
    
    if usuario_data.nombre is not None:
        updates.append("[nombre] = ?")
        params.append(usuario_data.nombre)
    
    if usuario_data.email is not None:
        updates.append("[email] = ?")
        params.append(usuario_data.email)
        
    # Si no hay nada que actualizar, devolvemos el objeto actual sin hacer query
    if not updates:
        return await get_one_u(id_usuario)

    updatescript = f"""
        UPDATE [music].[usuarios]
        SET {', '.join(updates)}
        WHERE [id_usuario] = ?;
    """
    
    # Agregamos el id_usuario al final de los parámetros
    params.append(id_usuario)

    try:
        # 1. Ejecutar el UPDATE
        await execute_query_json(updatescript, params=params, needs_commit=True)
        
        # 2. Obtener el objeto actualizado para devolverlo
        usuario_actualizado = await get_one_u(id_usuario)
        return usuario_actualizado
        
    except HTTPException:
        # Si get_one_u falla (404) o la validación del email falla (409), propagamos el error
        raise
    except Exception as e:
        # CORRECCIÓN CLAVE: Convertir el código de estado a string para usar 'in'
        if str(status.HTTP_409_CONFLICT) in str(e): # El manejador en utils/database.py lanza 409
            raise HTTPException(status_code=409, detail=f"El email ya está en uso por otro usuario.")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos al actualizar: { str(e) }")

# --- DELETE (DELETE /{id}) ---
async def delete_user(id_usuario: int) -> str:
    """Elimina un usuario por su ID."""
    
    deletescript = """
        DELETE FROM [music].[usuarios]
        WHERE [id_usuario] = ?;
    """

    params = [id_usuario]

    try:
        # 1. Verificamos si existe antes de intentar eliminar (para un 404 claro)
        await get_one_u(id_usuario)
        
        # 2. Ejecutamos el DELETE
        await execute_query_json(deletescript, params=params, needs_commit=True)
        
        return "DELETED"
        
    except HTTPException:
        # Propaga el 404 de get_one_u si no existe
        raise
    except Exception as e:
        # Manejo de error de clave foránea (si el usuario tiene playlists)
        if 'FOREIGN KEY' in str(e).upper():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el usuario porque tiene playlists u otros recursos asociados.")
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")





