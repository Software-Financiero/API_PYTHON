from flask import Blueprint
from src.controllers.macroeconomicos.desempleo import GetDesempleo, SaveDesempleo 
from src.controllers.predicciones.desempleo import prediccion_desempleo

bp = Blueprint("desempleo_routes", __name__)

path = '/indicadores/desempleo'

@bp.get(f"{path}/")
def list_Desempleo():
  return GetDesempleo()


@bp.post(f"{path}/")
def PostDesempleo():
  return SaveDesempleo()

@bp.get(f"{path}/prediccion")
def Pre_desempleo():
  return prediccion_desempleo()
