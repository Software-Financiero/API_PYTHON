from flask import Blueprint
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

@bp.get(f"{path}/prediccion")
def pre_PIB():
  return prediccion_pib()
