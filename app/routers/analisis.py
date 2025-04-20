# app/routers/analisis.py

from fastapi import APIRouter, HTTPException
from app.db import supabase
from app.analisis import calcular_puntaje, clasificar_grupo

router = APIRouter(
    prefix="/analisis",
    tags=["Análisis Socioeconómico"]
)

@router.get("/riesgo/{estudiante_id}")
async def calcular_riesgo(estudiante_id: str):
    # Obtener la información necesaria de Supabase
    vivienda = supabase.table("vivienda_tecnologia").select("*").eq("estudiante_id", estudiante_id).execute()

    if not vivienda.data:
        raise HTTPException(status_code=404, detail="Datos de vivienda no encontrados para este estudiante")

    datos_vivienda = vivienda.data[0]

    # Calcular el puntaje
    puntaje = calcular_puntaje(datos_vivienda)
    grupo = clasificar_grupo(puntaje)

    return {
        "id_estudiante": estudiante_id,
        "puntaje_total": puntaje,
        "grupo_socioeconomico": grupo
    }
