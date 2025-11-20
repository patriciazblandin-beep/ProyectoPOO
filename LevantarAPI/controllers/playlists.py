import logging
from typing import List, Optional
from fastapi import HTTPException, status
from models.playlists import PlaylistOut, PlaylistIn, PlaylistUpdate
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def _fetch_playlist_by_id(id_playlists: int) -> Optional[PlaylistOut]:
    sql = """
        SELECT [id_playlists], [id_usuario], [nombre], [fecha_creacion]
        FROM [music].[playlists]
        WHERE id_playlists = ?;
    """
    result = await execute_query_json(sql, params=[id_playlists], fetch_one=True)
    return PlaylistOut(**result) if result else None

async def create_playlist(data: PlaylistIn) -> PlaylistOut:
    sql = """
        INSERT INTO [music].[playlists] ([id_usuario], [nombre])
        VALUES (?, ?);
    """
    params = [data.id_usuario, data.nombre]

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
        sql_last = """
            SELECT TOP 1 [id_playlists], [id_usuario], [nombre], [fecha_creacion]
            FROM [music].[playlists]
            WHERE id_usuario = ? AND nombre = ?
            ORDER BY fecha_creacion DESC;
        """
        result = await execute_query_json(sql_last, params=params, fetch_one=True)
        if result:
            return PlaylistOut(**result)
        raise HTTPException(status_code=500, detail="Playlist creada pero no se pudo recuperar.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear playlist: {str(e)}")

async def get_all_playlists() -> List[PlaylistOut]:
    sql = """
        SELECT [id_playlists], [id_usuario], [nombre], [fecha_creacion]
        FROM [music].[playlists];
    """
    try:
        results = await execute_query_json(sql, fetch_all=True)
        return [PlaylistOut(**row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar playlists: {str(e)}")

# --- READ ONE ---
async def get_one_playlist(id_playlists: int) -> PlaylistOut:
    playlist = await _fetch_playlist_by_id(id_playlists)
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Playlist con ID {id_playlists} no encontrada.")
    return playlist

async def update_playlist(id_playlists: int, data: PlaylistUpdate) -> PlaylistOut:
    updates = []
    params = []

    if data.nombre is not None:
        updates.append("[nombre] = ?")
        params.append(data.nombre)

    if not updates:
        return await get_one_playlist(id_playlists)

    sql = f"""
        UPDATE [music].[playlists]
        SET {', '.join(updates)}
        WHERE [id_playlists] = ?;
    """
    params.append(id_playlists)

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
        return await get_one_playlist(id_playlists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar playlist: {str(e)}")

async def delete_playlist(id_playlists: int) -> str:
    await get_one_playlist(id_playlists) 

    sql = """
        DELETE FROM [music].[playlists]
        WHERE [id_playlists] = ?;
    """
    try:
        await execute_query_json(sql, params=[id_playlists], needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar playlist: {str(e)}")
