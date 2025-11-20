from fastapi import APIRouter, status, HTTPException
from typing import List
from models.playlists import PlaylistIn, PlaylistOut, PlaylistUpdate
from controllers import playlists as playlist_controller

router = APIRouter(
    tags=["Playlists"],
)

# 1. POST: Crear Nueva Playlist
@router.post("/", response_model=PlaylistOut, status_code=status.HTTP_201_CREATED, summary="Crea una nueva playlist")
async def create_playlist_route(playlist: PlaylistIn):
    return await playlist_controller.create_playlist(playlist)

# Obtener TODAS las Playlists

@router.get("/", response_model=List[PlaylistOut], summary="Obtiene todas las playlists")
async def get_all_playlists_route():
    return await playlist_controller.get_all_playlists()


# Obtener Playlist por Id

@router.get("/{id_playlists}", response_model=PlaylistOut, summary="obtiene una playlists por su ID")
async def get_playlist_by_id_route(id_playlists: int):
    return await playlist_controller.get_one_playlist(id_playlists)


#  Actualizar Playlist por ID

@router.put("/{id_playlists}", response_model=PlaylistOut, summary="Actualiza una playlist existente")
async def update_playlist_route(id_playlists: int, playlist: PlaylistUpdate):
    return await playlist_controller.update_playlist(id_playlists, playlist)

# 5. DELETE: Eliminar Playlist por ID

@router.delete("/{id_playlists}", status_code=status.HTTP_204_NO_CONTENT, summary="Elimina una playlist por su ID")
async def delete_playlist_route(id_playlists: int):
    deleted = await playlist_controller.delete_playlist(id_playlists)

    if deleted == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist no encontrada para eliminar.")

    return 