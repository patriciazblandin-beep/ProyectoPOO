from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models.artistas import ArtistaIn, ArtistaOut, ArtistaUpdate 
from controllers import artistas as artista_controller 

router = APIRouter(
    tags=["Artista"], 
)

# ----------------------------------------------------------------------
# 1. POST: Crear Nuevo atista
# ----------------------------------------------------------------------
@router.post("/", response_model=ArtistaOut, status_code=status.HTTP_201_CREATED, summary="Crea un nuevo artista (Requiere id_usuario)")
async def create_artista_route(artista: ArtistaIn):
    return await artista_controller.create_artistas(artista)

# ----------------------------------------------------------------------
# 2. GET: Obtener todos los atista
# ----------------------------------------------------------------------
@router.get("/", response_model=List[ArtistaOut], summary="Obtiene todos los artistas")
async def get_all_artistas_route():
    return await artista_controller.get_all_artistas()

# ----------------------------------------------------------------------
# 3. GET: Obtener atista por ID
# ----------------------------------------------------------------------
@router.get("/{id_artista}", response_model=ArtistaOut, summary="Obtiene un artista por su ID")
async def get_artistas_by_id_route(id_artista: int):
    artista = await artista_controller.get_one_p(id_artista) # Cambié a get_one_p que es el nombre en el controlador
    return artista 

# ----------------------------------------------------------------------
# 4. PUT: Actualizar atista por ID
# ----------------------------------------------------------------------
@router.put("/{id_artista}", response_model=ArtistaOut, summary="Actualiza el nombre de un artista existente")
async def update_artistas_route(id_artista: int, artista: ArtistaUpdate):
    updated_artista = await artista_controller.update_playlist(id_artista, artista)
    return updated_artista

# ----------------------------------------------------------------------
# 5. DELETE: Eliminar atista por ID
# ----------------------------------------------------------------------
@router.delete("/{artista}", status_code=status.HTTP_204_NO_CONTENT, summary="Elimina un artista por su ID")
async def delete_artistas_route(id_artista: int):
    # La función de control lanza 404 si no encuentra, así que no necesitamos el conteo aquí
    await artista_controller.delete_artistas(id_artista)
    return