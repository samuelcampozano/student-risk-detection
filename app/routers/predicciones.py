from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml import entrenar_modelo, predecir_grupo
from app.analisis import calcular_todos_los_estudiantes, calcular_puntaje

router = APIRouter(
    prefix="/predicciones",
    tags=["Predicciones"]
)

class DatosSocioeconomicos(BaseModel):
    tipo_vivienda: str
    material_paredes: str
    material_piso: str
    numero_banos: int
    servicio_higienico: str
    internet: bool
    computadora: bool
    laptop: bool
    celulares: int
    telefono_convencional: bool
    cocina_con_horno: bool
    refrigeradora: bool
    lavadora: bool
    equipo_sonido: bool
    tv_color: int
    vehiculos: int

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

@router.post("/predecir-datos/")
async def predecir_desde_datos(datos: DatosSocioeconomicos):
    puntaje = calcular_puntaje(datos.dict())
    grupo_predicho = predecir_grupo(puntaje)
    return {
        "puntaje_calculado": puntaje,
        "grupo_predicho": grupo_predicho
    }
