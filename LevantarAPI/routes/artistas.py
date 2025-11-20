from fastapi import APIRouter, status, HTTPException
from models.artistas import ArtistaIn, ArtistaOut, ArtistaUpdate
from controllers import artistas as artista_controller

router = APIRouter(tags=["Artistas"])

@router.post("/", response_model=ArtistaOut, status_code=status.HTTP_201_CREATED,  summary="Crea un artista")
async def create_artista_route(artista: ArtistaIn):
    return await artista_controller.create_artista(artista)

@router.get("/", response_model=list[ArtistaOut],  summary="Obtiene todos los artistas")
async def get_all_artistas_route():
    return await artista_controller.get_all_artistas()

@router.get("/{id_artista}", response_model=ArtistaOut,  summary="Obtiene un artista por su id")
async def get_artista_by_id_route(id_artista: int):
    return await artista_controller.get_one_artista(id_artista)

@router.put("/{id_artista}", response_model=ArtistaOut,  summary="actualiza un artista exitente")
async def update_artista_route(id_artista: int, artista: ArtistaUpdate):
    return await artista_controller.update_artista(id_artista, artista)

@router.delete("/{id_artista}", status_code=status.HTTP_204_NO_CONTENT,  summary="Crea un artista por su id ")
async def delete_artista_route(id_artista: int):
    deleted = await artista_controller.delete_artista(id_artista)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Artista no encontrado para eliminar.") 