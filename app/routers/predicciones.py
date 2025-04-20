from fastapi import APIRouter, HTTPException
from app.ml import entrenar_modelo, predecir_grupo
from app.analisis import calcular_todos_los_estudiantes

router = APIRouter(
    prefix="/predicciones",
    tags=["Predicciones"]
)

@router.post("/entrenar/")
async def entrenar():
    datos = await calcular_todos_los_estudiantes()

    if not datos:
        raise HTTPException(status_code=404, detail="No hay datos para entrenar el modelo")

    entrenar_modelo(datos)
    return {"mensaje": "Modelo entrenado exitosamente"}

@router.get("/predecir/{puntaje}")
async def predecir(puntaje: int):
    grupo_predicho = predecir_grupo(puntaje)
    return {"grupo_predicho": grupo_predicho}
