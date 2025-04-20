from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict
import numpy as np

modelo = None  # Variable global temporal

grupo_a_numero = {
    "Alto": 4,
    "Medio Alto": 3,
    "Medio Típico": 2,
    "Medio Bajo": 1,
    "Bajo": 0
}

numero_a_grupo = {v: k for k, v in grupo_a_numero.items()}

def entrenar_modelo(datos: List[Dict]):
    """
    Entrena un modelo Random Forest basado en los estudiantes ya analizados.
    """
    global modelo

    X = np.array([[dato["puntaje_total"]] for dato in datos])
    y = np.array([grupo_a_numero[dato["grupo_socioeconomico"]] for dato in datos])

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    modelo = rf

def predecir_grupo(puntaje: int) -> str:
    """
    Predice el grupo socioeconómico basado en el puntaje total.
    """
    if modelo is None:
        raise Exception("El modelo aún no ha sido entrenado")

    prediccion = modelo.predict(np.array([[puntaje]]))
    return numero_a_grupo[prediccion[0]]
