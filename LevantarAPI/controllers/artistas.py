from fastapi import HTTPException
from models.artistas import ArtistaIn, ArtistaOut, ArtistaUpdate
from utils.database import execute_query_json

async def create_artista(data: ArtistaIn) -> ArtistaOut:
    sql = "INSERT INTO music.artistas (nombre, discografica) VALUES (?, ?);"
    await execute_query_json(sql, params=[data.nombre, data.discografica], needs_commit=True)

    sql_last = "SELECT TOP 1 id_artista, nombre, discografica FROM music.artistas ORDER BY id_artista DESC;"
    result = await execute_query_json(sql_last, fetch_one=True)
    return ArtistaOut(**result)

async def get_all_artistas() -> list[ArtistaOut]:
    sql = "SELECT id_artista, nombre, discografica FROM music.artistas;"
    result = await execute_query_json(sql, fetch_all=True) 
    print("Artistas encontrados:", result)
    return [ArtistaOut(**row) for row in result]

async def get_one_artista(id_artista: int) -> ArtistaOut:
    sql = "SELECT id_artista, nombre, discografica FROM music.artistas WHERE id_artista = ?;"
    result = await execute_query_json(sql, params=[id_artista], fetch_one=True)
    if result:
        return ArtistaOut(**result)
    raise HTTPException(status_code=404, detail="Artista no encontrado.")

async def update_artista(id_artista: int, data: ArtistaUpdate) -> ArtistaOut:
    sql = "UPDATE music.artistas SET nombre = ?, discografica = ? WHERE id_artista = ?;"
    await execute_query_json(sql, params=[data.nombre, data.discografica, id_artista], needs_commit=True)
    return await get_one_artista(id_artista)

async def delete_artista(id_artista: int) -> int:
    sql = "DELETE FROM music.artistas WHERE id_artista = ?;"
    result = await execute_query_json(sql, params=[id_artista], needs_commit=True)
    return result 
