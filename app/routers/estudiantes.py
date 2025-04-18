from fastapi import APIRouter
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
