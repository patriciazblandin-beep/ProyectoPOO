from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models.playlists import PlaylistIn, PlaylistOut, PlaylistUpdate 
from controllers import playlists as playlist_controller 

# Define el router (SIN prefijo porque se añade en main.py)
router = APIRouter(
    tags=["Playlists"], # <--- ESTO ES CRUCIAL
)

# ----------------------------------------------------------------------
# 1. POST: Crear Nueva Playlist
# ----------------------------------------------------------------------
@router.post("/", response_model=PlaylistOut, status_code=status.HTTP_201_CREATED, summary="Crea una nueva playlist (Requiere id_usuario)")
async def create_playlist_route(playlist: PlaylistIn):
    return await playlist_controller.create_playlist(playlist)

# ----------------------------------------------------------------------
# 2. GET: Obtener TODAS las Playlists
# ----------------------------------------------------------------------
@router.get("/", response_model=List[PlaylistOut], summary="Obtiene todas las playlists")
async def get_all_playlists_route():
    return await playlist_controller.get_all_playlists()

# ----------------------------------------------------------------------
# 3. GET: Obtener Playlist por ID
# ----------------------------------------------------------------------
@router.get("/{id_playlists}", response_model=PlaylistOut, summary="Obtiene una playlist por su ID")
async def get_playlist_by_id_route(id_playlists: int):
    playlist = await playlist_controller.get_one_p(id_playlists) # Cambié a get_one_p que es el nombre en el controlador
    return playlist 

# ----------------------------------------------------------------------
# 4. PUT: Actualizar Playlist por ID
# ----------------------------------------------------------------------
@router.put("/{id_playlists}", response_model=PlaylistOut, summary="Actualiza el nombre de una playlist existente")
async def update_playlist_route(id_playlists: int, playlist: PlaylistUpdate):
    updated_playlist = await playlist_controller.update_playlist(id_playlists, playlist)
    return updated_playlist 

# ----------------------------------------------------------------------
# 5. DELETE: Eliminar Playlist por ID
# ----------------------------------------------------------------------
@router.delete("/{id_playlists}", status_code=status.HTTP_204_NO_CONTENT, summary="Elimina una playlist por su ID")
async def delete_playlist_route(id_playlists: int):
    # La función de control lanza 404 si no encuentra, así que no necesitamos el conteo aquí
    await playlist_controller.delete_playlist(id_playlists)
    return
