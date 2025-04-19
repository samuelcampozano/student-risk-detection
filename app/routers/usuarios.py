from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db import supabase
from app.auth import hashear_password, verificar_password, crear_token_acceso
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

class UsuarioRegistro(BaseModel):
    email: str
    password: str
    nombre_completo: str

class UsuarioToken(BaseModel):
    access_token: str
    token_type: str

@router.post("/registro", response_model=UsuarioToken)
async def registrar_usuario(usuario: UsuarioRegistro):
    existing = supabase.table("usuarios").select("id").eq("email", usuario.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    hashed_password = hashear_password(usuario.password)
    nuevo_usuario = {
        "email": usuario.email,
        "hashed_password": hashed_password,
        "nombre_completo": usuario.nombre_completo
    }
    response = supabase.table("usuarios").insert(nuevo_usuario).execute()

    token = crear_token_acceso({"sub": response.data[0]["id"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=UsuarioToken)
async def login_usuario(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    usuario = supabase.table("usuarios").select("*").eq("email", email).execute()
    if not usuario.data:
        raise HTTPException(status_code=400, detail="Email incorrecto")

    usuario_db = usuario.data[0]
    if not verificar_password(password, usuario_db["hashed_password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = crear_token_acceso({"sub": usuario_db["id"]})
    return {"access_token": token, "token_type": "bearer"}
