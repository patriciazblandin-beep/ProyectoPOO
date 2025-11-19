from fastapi import FastAPI

# ----------------------------------------------------------------------
from routes.usuarios import router as usuarios_router
from routes.playlists import router as playlists_router 
from routes.artistas  import router as artista_router


# Inicialización de la aplicación FastAPI
app = FastAPI()

app.include_router(usuarios_router, prefix="/usuarios")
app.include_router(playlists_router, prefix="/playlists")
app.include_router(artista_router, prefix="/artistas")


# Ruta raíz simple para verificar que la API está viv
@app.get("/")
def read_root():
    return {"message": "API de música activa."}