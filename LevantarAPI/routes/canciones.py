from fastapi import APIRouter, status, HTTPException
from models.canciones import CancionIn, CancionOut, CancionUpdate
from controllers import canciones as cancion_controller

router = APIRouter(tags=["Canciones"])  # etiqueta para Swagger

# crear una canción
@router.post("/", response_model=CancionOut, status_code=status.HTTP_201_CREATED, summary="Crea una concion ")
async def create_cancion_route(cancion: CancionIn):
    return await cancion_controller.create_cancion(cancion)

# poder vet todas las canciones
@router.get("/", response_model=list[CancionOut], summary="Obtiene todas las canciones")
async def get_all_canciones_route():
    return await cancion_controller.get_all_canciones()

# poder ver una canción por ID
@router.get("/{id_cancion}", response_model=CancionOut, summary="Ver una cancion por su id")
async def get_cancion_by_id_route(id_cancion: int):
    return await cancion_controller.get_one_cancion(id_cancion)

# actualizar una canción
@router.put("/{id_cancion}", response_model=CancionOut, summary="Actualiza una cancion existente")
async def update_cancion_route(id_cancion: int, cancion: CancionUpdate):
    return await cancion_controller.update_cancion(id_cancion, cancion)

# para la eliminacion
@router.delete("/{id_cancion}", status_code=status.HTTP_204_NO_CONTENT, summary="Elimina uns cancion")
async def delete_cancion_route(id_cancion: int):
    deleted = await cancion_controller.delete_cancion(id_cancion)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Canción no encontrada para poder eliminar.") 