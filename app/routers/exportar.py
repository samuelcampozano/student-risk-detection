from fastapi import APIRouter, Response
from app.db import supabase
import pandas as pd
import io

router = APIRouter(
    prefix="/exportar",
    tags=["Exportar Datos"]
)

@router.get("/riesgos-excel/")
async def exportar_riesgos_excel():
    # Obtener los datos de vivienda
    vivienda_response = supabase.table("vivienda_tecnologia").select("*").execute()

    if not vivienda_response.data:
        return {"error": "No hay datos para exportar"}

    resultados = []
    for datos_vivienda in vivienda_response.data:
        estudiante_id = datos_vivienda.get("estudiante_id")
        
        from app.analisis import calcular_puntaje, clasificar_grupo
        puntaje = calcular_puntaje(datos_vivienda)
        grupo = clasificar_grupo(puntaje)

        resultados.append({
            "id_estudiante": estudiante_id,
            "puntaje_total": puntaje,
            "grupo_socioeconomico": grupo
        })

    # Convertir a DataFrame
    df = pd.DataFrame(resultados)

    # Guardar en un Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Riesgos")

    output.seek(0)

    # Devolver como archivo descargable
    headers = {
        'Content-Disposition': 'attachment; filename="riesgos_estudiantes.xlsx"'
    }
    return Response(content=output.read(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
