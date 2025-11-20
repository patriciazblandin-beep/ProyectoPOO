from fastapi import FastAPI

# ----------------------------------------------------------------------
from routes.usuarios import router as usuarios_router
from routes import playlists
from routes import artistas
from routes import albumes
from routes import canciones


# Inicialización de la aplicación FastAPI
app = FastAPI()

app.include_router(usuarios_router, prefix="/usuarios")
app.include_router(playlists.router, prefix="/playlists")
app.include_router(artistas.router, prefix="/artistas")
app.include_router(albumes.router, prefix="/albumes")
app.include_router(canciones.router, prefix="/canciones")



# Ruta raíz simple para verificar que la API está viv
@app.get("/")
def read_root():
    return {"message": "API de música activa 1."}  