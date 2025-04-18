from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(
    prefix="/vivienda",
    tags=["Vivienda y Tecnología"]
)

@router.post("/")
def crear_vivienda(data: dict):
    response = supabase.table('vivienda_tecnologia').insert(data).execute()
    return response.data

@router.get("/")
def listar_viviendas():
    response = supabase.table('vivienda_tecnologia').select("*").execute()
    return response.data

@router.get("/{vivienda_id}")
def obtener_vivienda(vivienda_id: str):
    response = supabase.table('vivienda_tecnologia').select("*").eq("id", vivienda_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada")
    return response.data[0]

@router.put("/{vivienda_id}")
def actualizar_vivienda(vivienda_id: str, data: dict):
    response = supabase.table('vivienda_tecnologia').update(data).eq("id", vivienda_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada o no actualizada")
    return response.data[0]

@router.delete("/{vivienda_id}")
def eliminar_vivienda(vivienda_id: str):
    response = supabase.table('vivienda_tecnologia').delete().eq("id", vivienda_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Vivienda no encontrada o no eliminada")
    return {"message": "Vivienda eliminada exitosamente"}
