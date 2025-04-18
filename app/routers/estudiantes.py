from fastapi import APIRouter, HTTPException
from app.models import Estudiante
from app.db import supabase

router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)

@router.post("/")
def crear_estudiante(estudiante: Estudiante):
    data = estudiante.dict()
    response = supabase.table('estudiantes').insert(data).execute()
    return response.data

@router.get("/")
def listar_estudiantes():
    response = supabase.table('estudiantes').select("*").execute()
    return response.data

@router.get("/{estudiante_id}")
def obtener_estudiante(estudiante_id: str):
    response = supabase.table('estudiantes').select("*").eq("id", estudiante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return response.data[0]

@router.put("/{estudiante_id}")
def actualizar_estudiante(estudiante_id: str, estudiante: Estudiante):
    data = estudiante.dict(exclude_unset=True)
    response = supabase.table('estudiantes').update(data).eq("id", estudiante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o no actualizado")
    return response.data[0]

@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: str):
    response = supabase.table('estudiantes').delete().eq("id", estudiante_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o no eliminado")
    return {"message": "Estudiante eliminado exitosamente"}
