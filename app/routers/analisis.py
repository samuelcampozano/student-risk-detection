from fastapi import APIRouter, HTTPException
from app.db import supabase
from app.analisis import calcular_puntaje, clasificar_grupo, calcular_todos_los_estudiantes, resumen_por_grupo

router = APIRouter(
    prefix="/analisis",
    tags=["Análisis Socioeconómico"]
)

@router.get("/riesgo/{estudiante_id}")
async def calcular_riesgo(estudiante_id: str):
    vivienda = supabase.table("vivienda_tecnologia").select("*").eq("estudiante_id", estudiante_id).execute()

    if not vivienda.data:
        raise HTTPException(status_code=404, detail="Datos de vivienda no encontrados para este estudiante")

    datos_vivienda = vivienda.data[0]
    puntaje = calcular_puntaje(datos_vivienda)
    grupo = clasificar_grupo(puntaje)

    return {
        "id_estudiante": estudiante_id,
        "puntaje_total": puntaje,
        "grupo_socioeconomico": grupo
    }

@router.get("/riesgos-todos/")
async def calcular_riesgos_todos():
    """
    Calcula el riesgo socioeconómico para todos los estudiantes.
    """
    resultados = await calcular_todos_los_estudiantes()
    return resultados

@router.get("/resumen/")
async def resumen_global():
    """
    Devuelve el resumen de cuántos estudiantes hay en cada grupo.
    """
    resumen = await resumen_por_grupo()
    return resumen
