from flask import Blueprint, request
from src.controllers.macroeconomicos.PIB import GetPIB, SavePIB 
from src.controllers.predicciones.pib import prediccion_pib 

bp = Blueprint("PIB_routes", __name__)

path = '/indicadores/PIB'

@bp.get(f"{path}")
def list_PIB():
  return GetPIB()


@bp.post(f"{path}")
def PostPIB():
  return SavePIB()

@bp.post(f"{path}/prediccion")
def pre_PIB():
  date = request.get_json()['date']
  return prediccion_pib(date)
