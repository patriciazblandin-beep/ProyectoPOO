from fastapi import HTTPException
from models.canciones import CancionIn, CancionOut, CancionUpdate
from utils.database import execute_query_json

# Crear una canción nueva
async def create_cancion(data: CancionIn) -> CancionOut:
    sql = """
        INSERT INTO music.canciones (id_album, titulo, duracion)
        VALUES (?, ?, ?);
    """
    await execute_query_json(sql, params=[data.id_album, data.titulo, data.duracion], needs_commit=True)

    # Traer la última canción insertada
    sql_last = """
        SELECT TOP 1 id_cancion, id_album, titulo, duracion
        FROM music.canciones ORDER BY id_cancion DESC;
    """
    result = await execute_query_json(sql_last, fetch_one=True)
    return CancionOut(**result)

# para poder obtener  todas las canciones
async def get_all_canciones() -> list[CancionOut]:
    sql = "SELECT id_cancion, id_album, titulo, duracion FROM music.canciones;"
    result = await execute_query_json(sql, fetch_all=True)
    return [CancionOut(**row) for row in result]

# Obtener una canción por el id
async def get_one_cancion(id_cancion: int) -> CancionOut:
    sql = "SELECT id_cancion, id_album, titulo, duracion FROM music.canciones WHERE id_cancion = ?;"
    result = await execute_query_json(sql, params=[id_cancion], fetch_one=True)
    if result:
        return CancionOut(**result)
    raise HTTPException(status_code=404, detail="Canción no encontrada.")

# actualizar una canción
async def update_cancion(id_cancion: int, data: CancionUpdate) -> CancionOut:
    sql = """
        UPDATE music.canciones
        SET id_album = ?, titulo = ?, duracion = ?
        WHERE id_cancion = ?;
    """
    await execute_query_json(sql, params=[data.id_album, data.titulo, data.duracion, id_cancion], needs_commit=True)
    return await get_one_cancion(id_cancion)

# para eliminar uns cancion
async def delete_cancion(id_cancion: int) -> int:
    sql = "DELETE FROM music.canciones WHERE id_cancion = ?;"
    result = await execute_query_json(sql, params=[id_cancion], needs_commit=True)
    return result 