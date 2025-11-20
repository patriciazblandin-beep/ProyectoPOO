from fastapi import APIRouter, status, HTTPException
from typing import List
# IMPORTANTE: La importación ahora es correcta con UsuarioOut y UsuarioUpdate
from models.usuarios import UsuarioIn, UsuarioOut, UsuarioUpdate 
from controllers import usuarios as user_controller
from datetime import datetime

# Define el router con un prefijo y tags
# CAMBIO 1: ELIMINAR el parámetro prefix del APIRouter.
# Esto evita que se genere /usuarios/usuarios/
router = APIRouter(
    tags=["Usuarios"],
)

# Crear Nuevo Usuario
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED, summary="Crea un nuevo usuario")
async def create_user_route(usuario: UsuarioIn):
    # Llama al controlador para crear y obtener el objeto completo
    return await user_controller.create_user(usuario)

#  Obtener TODOS los Usuarios
@router.get("/", response_model=List[UsuarioOut], summary="Obtiene todos los usuarios")
async def get_all_users_route():
    # Llama al controlador para obtener la lista de usuarios
    return await user_controller.get_all_u()


#  Obtener Usuario por ID

@router.get("/{id_usuario}", response_model=UsuarioOut, summary="Obtiene un usuario por su ID")
async def get_user_by_id_route(id_usuario: int):
    # Llama al controlador. Si no existe, el controlador lanza un 404
    return await user_controller.get_one_u(id_usuario)


#  Actualizar Usuario por ID
@router.put("/{id_usuario}", response_model=UsuarioOut, summary="Actualiza un usuario existente")
async def update_user_route(id_usuario: int, usuario: UsuarioUpdate):
    # Llama al controlador. Si no existe o hay conflicto de email, el controlador lanza el error
    return await user_controller.update_user(id_usuario, usuario)

#  Eliminar Usuario por ID

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT, summary="Elimina un usuario por su ID")
async def delete_user_route(id_usuario: int):
    
    deleted_count = await user_controller.delete_user(id_usuario)
    
    
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar.")

    return