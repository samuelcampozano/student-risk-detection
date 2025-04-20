from app.db import supabase

def calcular_puntaje(datos: dict) -> int:
    """
    Calcula el puntaje total basado en los datos socioeconómicos.
    """
    puntaje = 0

    # Tipo de vivienda
    tipo_vivienda = datos.get("tipo_vivienda")
    if tipo_vivienda in ["Suite de lujo", "Cuarto(s) en casa de inquilinato", "Departamento en casa o edificio", "Casa/Villa"]:
        puntaje += 59
    elif tipo_vivienda == "Mediagua":
        puntaje += 40
    elif tipo_vivienda == "Rancho":
        puntaje += 4
    elif tipo_vivienda == "Choza/Covacha/Otro":
        puntaje += 0

    # Material de paredes
    material_paredes = datos.get("material_paredes")
    if material_paredes == "Hormigón":
        puntaje += 59
    elif material_paredes == "Ladrillo o bloque":
        puntaje += 55
    elif material_paredes == "Adobe/ Tapia":
        puntaje += 47
    elif material_paredes == "Caña revestida o bahareque/ Madera":
        puntaje += 17
    elif material_paredes == "Caña no revestida/ Otros materiales":
        puntaje += 0

    # Material de piso
    material_piso = datos.get("material_piso")
    if material_piso == "Duela, parquet, tablón o piso flotante":
        puntaje += 48
    elif material_piso == "Cerámica, baldosa, vinil o marmetón":
        puntaje += 46
    elif material_piso == "Ladrillo o cemento":
        puntaje += 34
    elif material_piso == "Tabla sin tratar":
        puntaje += 32
    elif material_piso == "Tierra/ Caña/ Otros materiales":
        puntaje += 0

    # Número de baños
    numero_banos = datos.get("numero_banos", 0)
    if numero_banos == 1:
        puntaje += 12
    elif numero_banos == 2:
        puntaje += 24
    elif numero_banos >= 3:
        puntaje += 32

    # Servicio higiénico
    servicio_higienico = datos.get("servicio_higienico")
    if servicio_higienico == "Letrina":
        puntaje += 15
    elif servicio_higienico == "Con descarga directa al mar, río, lago o quebrada" or servicio_higienico == "Conectado a pozo ciego":
        puntaje += 18
    elif servicio_higienico == "Conectado a pozo séptico":
        puntaje += 22
    elif servicio_higienico == "Conectado a red pública de alcantarillado":
        puntaje += 38

    # Servicios tecnológicos
    if datos.get("internet"):
        puntaje += 45
    if datos.get("computadora"):
        puntaje += 35
    if datos.get("laptop"):
        puntaje += 39

    # Cantidad de celulares
    celulares = datos.get("celulares", 0)
    if celulares == 1:
        puntaje += 8
    elif celulares == 2:
        puntaje += 22
    elif celulares == 3:
        puntaje += 32
    elif celulares >= 4:
        puntaje += 42

    # Otros bienes
    if datos.get("telefono_convencional"):
        puntaje += 19
    if datos.get("cocina_con_horno"):
        puntaje += 29
    if datos.get("refrigeradora"):
        puntaje += 30
    if datos.get("lavadora"):
        puntaje += 18
    if datos.get("equipo_sonido"):
        puntaje += 18

    # Televisores
    tv_color = datos.get("tv_color", 0)
    if tv_color == 1:
        puntaje += 9
    elif tv_color == 2:
        puntaje += 23
    elif tv_color >= 3:
        puntaje += 34

    # Vehículos
    vehiculos = datos.get("vehiculos", 0)
    if vehiculos == 1:
        puntaje += 6
    elif vehiculos == 2:
        puntaje += 11
    elif vehiculos >= 3:
        puntaje += 15

    return puntaje

def clasificar_grupo(puntaje: int) -> str:
    """
    Clasifica al estudiante según su puntaje.
    """
    if puntaje >= 845:
        return "Alto"
    elif puntaje >= 696:
        return "Medio Alto"
    elif puntaje >= 535:
        return "Medio Típico"
    elif puntaje >= 326:
        return "Medio Bajo"
    else:
        return "Bajo"

async def calcular_todos_los_estudiantes():
    """
    Analiza todos los estudiantes registrados en Supabase
    y clasifica a cada uno en un grupo socioeconómico.
    """
    vivienda_response = supabase.table("vivienda_tecnologia").select("*").execute()

    if not vivienda_response.data:
        return []

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

async def resumen_por_grupo():
    """
    Devuelve un resumen de cuántos estudiantes hay en cada grupo socioeconómico.
    """
    resultados = await calcular_todos_los_estudiantes()
    resumen = {
        "Alto": 0,
        "Medio Alto": 0,
        "Medio Típico": 0,
        "Medio Bajo": 0,
        "Bajo": 0
    }

    for estudiante in resultados:
        grupo = estudiante["grupo_socioeconomico"]
        resumen[grupo] += 1

    return resumen