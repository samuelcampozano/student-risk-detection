from fastapi import FastAPI
from app.routers import estudiantes, representantes, vivienda_tecnologia, bienes_habitos, actividad_economica, usuarios

app = FastAPI(title="Sistema Minería Educacional")

# Routers
app.include_router(estudiantes.router)
app.include_router(representantes.router)
app.include_router(vivienda_tecnologia.router)
app.include_router(bienes_habitos.router)
app.include_router(actividad_economica.router)
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {"message": "API de Minería Educacional funcionando"}
