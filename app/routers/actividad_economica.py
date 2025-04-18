from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(
    prefix="/actividad-economica",
    tags=["Actividad Económica"]
)

@router.post("/")
def crear_actividad(data: dict):
    response = supabase.table('actividad_economica').insert(data).execute()
    return response.data

@router.get("/")
def listar_actividades():
    response = supabase.table('actividad_economica').select("*").execute()
    return response.data

@router.get("/{actividad_id}")
def obtener_actividad(actividad_id: str):
    response = supabase.table('actividad_economica').select("*").eq("id", actividad_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return response.data[0]

@router.put("/{actividad_id}")
def actualizar_actividad(actividad_id: str, data: dict):
    response = supabase.table('actividad_economica').update(data).eq("id", actividad_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Actividad no encontrada o no actualizada")
    return response.data[0]

@router.delete("/{actividad_id}")
def eliminar_actividad(actividad_id: str):
    response = supabase.table('actividad_economica').delete().eq("id", actividad_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Actividad no encontrada o no eliminada")
    return {"message": "Actividad eliminada exitosamente"}
