from fastapi import APIRouter, status, HTTPException
from models.albumes import AlbumIn, AlbumOut, AlbumUpdate
from controllers import albumes as album_controller

router = APIRouter(tags=["Álbumes"])

@router.post("/", response_model=AlbumOut, status_code=status.HTTP_201_CREATED,  summary="Crea un album ")
async def create_album_route(album: AlbumIn):
    return await album_controller.create_album(album)

@router.get("/", response_model=list[AlbumOut],  summary="Obtiene todos los albumes")
async def get_all_albumes_route():
    return await album_controller.get_all_albumes()

@router.get("/{id_album}", response_model=AlbumOut,  summary="Obtiene un album por su id ")
async def get_album_by_id_route(id_album: int):
    return await album_controller.get_one_album(id_album)

@router.put("/{id_album}", response_model=AlbumOut, summary="Actualiza un album por su id")
async def update_album_route(id_album: int, album: AlbumUpdate):
    return await album_controller.update_album(id_album, album)

@router.delete("/{id_album}", status_code=status.HTTP_204_NO_CONTENT,  summary="Elimina un album por su id")
async def delete_album_route(id_album: int):
    deleted = await album_controller.delete_album(id_album)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Álbum no encontrado para eliminar.")