from fastapi import APIRouter, HTTPException
from app.db import supabase

router = APIRouter(
    prefix="/representantes",
    tags=["Representantes"]
)

@router.post("/")
def crear_representante(data: dict):
    response = supabase.table('representantes').insert(data).execute()
    return response.data

@router.get("/")
def listar_representantes():
    response = supabase.table('representantes').select("*").execute()
    return response.data

@router.get("/{representante_id}")
def obtener_representante(representante_id: str):
    response = supabase.table('representantes').select("*").eq("id", representante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Representante no encontrado")
    return response.data[0]

@router.put("/{representante_id}")
def actualizar_representante(representante_id: str, data: dict):
    response = supabase.table('representantes').update(data).eq("id", representante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Representante no encontrado o no actualizado")
    return response.data[0]

@router.delete("/{representante_id}")
def eliminar_representante(representante_id: str):
    response = supabase.table('representantes').delete().eq("id", representante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Representante no encontrado o no eliminado")
    return {"message": "Representante eliminado exitosamente"}
