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
async def calcular_riesgos_todos(skip: int = 0, limit: int = 10):
    """
    Calcula el riesgo socioeconómico para todos los estudiantes, con paginación.
    """
    vivienda_response = supabase.table("vivienda_tecnologia").select("*").range(skip, skip + limit - 1).execute()

    if not vivienda_response.data:
        raise HTTPException(status_code=404, detail="No hay más estudiantes")

    resultados = []
    for datos_vivienda in vivienda_response.data:
        estudiante_id = datos_vivienda.get("estudiante_id")
        puntaje = calcular_puntaje(datos_vivienda)
        grupo = clasificar_grupo(puntaje)

        resultados.append({
            "id_estudiante": estudiante_id,
            "puntaje_total": puntaje,
            "grupo_socioeconomico": grupo
        })

    return resultados


@router.get("/resumen/")
async def resumen_global():
    resumen = await resumen_por_grupo()

    total_estudiantes = sum(resumen.values())
    bajo_riesgo = resumen.get("Bajo", 0)

    alerta = None
    if total_estudiantes > 0 and (bajo_riesgo / total_estudiantes) >= 0.3:
        alerta = "⚠️ Alerta: Más del 30% de estudiantes están en riesgo socioeconómico bajo."

    return {
        "resumen": resumen,
        "alerta": alerta
    }

