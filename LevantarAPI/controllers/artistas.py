from models.artistas import ArtistaIn, ArtistaOut, ArtistaUpdate
from typing import List
from fastapi import HTTPException, status
import logging

# Configuración básica de logging
logger = logging.getLogger(__name__)

# Base de datos simulada para Playlists (Se reemplazará por SQL Server)
_artistas = {}
_next_id = 1

def _check_artistas_exists(artista_id: int):
    """Verifica si una playlist existe y levanta 404 si no."""
    if artista_id not in _artistas :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artista con ID {artista_id} no encontrada."
        )

# ----------------------------------------------------------------------
# Lógica de Negocio
# ----------------------------------------------------------------------

# 1. CREAR PLAYLIST
async def create_artistas(artista: ArtistaIn) -> ArtistaOut:
    """Crea un nuevo artista en la base de datos simulada."""
    global _next_id
    
    new_id = _next_id
    _next_id += 1
    
    nueva_artista = ArtistaOut(
        id_artista=new_id,
        nombre=artista.nombre,
        discografica=artista.discografica,
    )
    _artistas[new_id] = nueva_artista.model_dump()
    
    logger.info(f"artista creada con ID: {new_id}")
    return nueva_artista

# 2. OBTENER TODAS
async def get_all_artistas() -> List[ArtistaOut]:
    """Obtiene todos los artistas."""
    # Simular consulta a SQL Server
    return [ArtistaOut(**data) for data in _artistas.values()]

# 3. OBTENER UNA
async def get_one_a(artista_id: int) -> ArtistaOut:
    """Obtiene un artista por su ID."""
    _check_artistas_exists(artista_id)
    return artista_id(**_artistas[artista_id])

# 4. ACTUALIZAR
async def update_artistas(artista_id: int, artista_update: ArtistaUpdate) -> ArtistaOut:
    """Actualiza un artista por su ID."""
    _check_artistas_exists(artista_id)
    
    current_data = _artistas[artista_id]
    updated_fields = artista_update.model_dump(exclude_unset=True)
    current_data.update(updated_fields)
    
    _artistas[artista_id] = current_data
    
    logger.info(f"Playlist con ID {artista_id} actualizada.")
    return ArtistaOut(**current_data)

# 5. ELIMINAR
async def delete_playlist(artista_id: int) -> int:
    """Elimina un artista por su ID."""
    _check_artistas_exists(artista_id)
    
    del _artistas[artista_id]
    
    logger.info(f"artista con ID {artista_id} eliminada.")
    return 1
