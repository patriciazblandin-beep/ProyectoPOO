from models.playlists import PlaylistIn, PlaylistOut, PlaylistUpdate
from typing import List
from fastapi import HTTPException, status
from datetime import datetime
import logging

# Configuración básica de logging
logger = logging.getLogger(__name__)

# Base de datos simulada para Playlists (Se reemplazará por SQL Server)
_playlists = {}
_next_id = 1

def _check_playlist_exists(playlist_id: int):
    """Verifica si una playlist existe y levanta 404 si no."""
    if playlist_id not in _playlists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Playlist con ID {playlist_id} no encontrada."
        )

# ----------------------------------------------------------------------
# Lógica de Negocio
# ----------------------------------------------------------------------

# 1. CREAR PLAYLIST
async def create_playlist(playlist: PlaylistIn) -> PlaylistOut:
    """Crea una nueva playlist en la base de datos simulada."""
    global _next_id
    
    # Simular la inserción en SQL Server
    new_id = _next_id
    _next_id += 1
    
    nueva_playlist = PlaylistOut(
        id_playlists=new_id,
        nombre=playlist.nombre,
        id_usuario=playlist.id_usuario,
        descripcion=playlist.descripcion,
        fecha_creacion=datetime.now() # Fecha de creación simulada
    )
    _playlists[new_id] = nueva_playlist.model_dump()
    
    logger.info(f"Playlist creada con ID: {new_id}")
    return nueva_playlist

# 2. OBTENER TODAS
async def get_all_playlists() -> List[PlaylistOut]:
    """Obtiene todas las playlists."""
    # Simular consulta a SQL Server
    return [PlaylistOut(**data) for data in _playlists.values()]

# 3. OBTENER UNA
async def get_one_p(playlist_id: int) -> PlaylistOut:
    """Obtiene una playlist por su ID."""
    _check_playlist_exists(playlist_id)
    # Simular consulta a SQL Server
    return PlaylistOut(**_playlists[playlist_id])

# 4. ACTUALIZAR
async def update_playlist(playlist_id: int, playlist_update: PlaylistUpdate) -> PlaylistOut:
    """Actualiza una playlist por su ID."""
    _check_playlist_exists(playlist_id)
    
    current_data = _playlists[playlist_id]
    updated_fields = playlist_update.model_dump(exclude_unset=True)
    current_data.update(updated_fields)
    
    _playlists[playlist_id] = current_data
    
    logger.info(f"Playlist con ID {playlist_id} actualizada.")
    return PlaylistOut(**current_data)

# 5. ELIMINAR
async def delete_playlist(playlist_id: int) -> int:
    """Elimina una playlist por su ID."""
    _check_playlist_exists(playlist_id)
    
    del _playlists[playlist_id]
    
    logger.info(f"Playlist con ID {playlist_id} eliminada.")
    return 1
