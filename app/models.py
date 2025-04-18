from pydantic import BaseModel
from typing import Optional

class Estudiante(BaseModel):
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[str] = None
    edad: Optional[int] = None
    cedula: Optional[str] = None
    telefono: Optional[str] = None
    grado: Optional[str] = None
    direccion: Optional[str] = None
    escuela_procedencia: Optional[str] = None
