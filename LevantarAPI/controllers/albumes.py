from fastapi import HTTPException
from models.albumes import AlbumIn, AlbumOut, AlbumUpdate
from utils.database import execute_query_json

async def create_album(data: AlbumIn) -> AlbumOut:
    sql = """
        INSERT INTO music.albumes (id_artista, titulo, fecha_lanzamiento)
        VALUES (?, ?, ?);
    """
    await execute_query_json(sql, params=[data.id_artista, data.titulo, data.fecha_lanzamiento], needs_commit=True)

    sql_last = """
        SELECT TOP 1 id_album, id_artista, titulo, fecha_lanzamiento
        FROM music.albumes ORDER BY id_album DESC;
    """
    result = await execute_query_json(sql_last, fetch_one=True)
    return AlbumOut(**result)

async def get_all_albumes() -> list[AlbumOut]:
    sql = "SELECT id_album, id_artista, titulo, fecha_lanzamiento FROM music.albumes;"
    result = await execute_query_json(sql, fetch_all=True)
    return [AlbumOut(**row) for row in result]

async def get_one_album(id_album: int) -> AlbumOut:
    sql = "SELECT id_album, id_artista, titulo, fecha_lanzamiento FROM music.albumes WHERE id_album = ?;"
    result = await execute_query_json(sql, params=[id_album], fetch_one=True)
    if result:
        return AlbumOut(**result)
    raise HTTPException(status_code=404, detail="Álbum no encontrado.")

async def update_album(id_album: int, data: AlbumUpdate) -> AlbumOut:
    sql = """
        UPDATE music.albumes
        SET id_artista = ?, titulo = ?, fecha_lanzamiento = ?
        WHERE id_album = ?;
    """
    await execute_query_json(sql, params=[data.id_artista, data.titulo, data.fecha_lanzamiento, id_album], needs_commit=True)
    return await get_one_album(id_album)

async def delete_album(id_album: int) -> int:
    sql = "DELETE FROM music.albumes WHERE id_album = ?;"
    result = await execute_query_json(sql, params=[id_album], needs_commit=True)
    return result 