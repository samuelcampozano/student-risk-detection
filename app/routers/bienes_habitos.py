from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(
    prefix="/bienes",
    tags=["Bienes y Hábitos"]
)

@router.post("/")
def crear_bienes(data: dict):
    response = supabase.table('bienes_habitos').insert(data).execute()
    return response.data

@router.get("/")
def listar_bienes():
    response = supabase.table('bienes_habitos').select("*").execute()
    return response.data

@router.get("/{bien_id}")
def obtener_bien(bien_id: str):
    response = supabase.table('bienes_habitos').select("*").eq("id", bien_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    return response.data[0]

@router.put("/{bien_id}")
def actualizar_bien(bien_id: str, data: dict):
    response = supabase.table('bienes_habitos').update(data).eq("id", bien_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Bien no encontrado o no actualizado")
    return response.data[0]

@router.delete("/{bien_id}")
def eliminar_bien(bien_id: str):
    response = supabase.table('bienes_habitos').delete().eq("id", bien_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Bien no encontrado o no eliminado")
    return {"message": "Bien eliminado exitosamente"}
