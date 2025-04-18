from fastapi import FastAPI
from app.routers import estudiantes

app = FastAPI(title="Sistema Minería Educacional")

# Incluimos las rutas
app.include_router(estudiantes.router)

@app.get("/")
def read_root():
    return {"message": "API de Minería Educacional funcionando"}
