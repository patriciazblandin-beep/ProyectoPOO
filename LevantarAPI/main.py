from fastapi import FastAPI
# ----------------------------------------------------------------------
# 1. Importación EXPLICITA del objeto 'router' de cada archivo
# Esto es más robusto que "from routes import usuarios"
# ----------------------------------------------------------------------
from routes.usuarios import router as usuarios_router
from routes.playlists import router as playlists_router

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Incluir los routers
app.include_router(usuarios_router, prefix="/usuarios")
app.include_router(playlists_router, prefix="/playlists")

# Ruta raíz simple para verificar que la API está viva
@app.get("/")
def read_root():
    return {"message": "API de música activa."}
