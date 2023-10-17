from flask import Blueprint
from src.controllers.macroeconomicos.inflacion import GetInflacion, SaveInflacion 
from src.controllers.predicciones.inflacion import prediccion_inflacion

bp = Blueprint("inflacion_routes", __name__)

path = '/indicadores/inflacion'

@bp.get(f"{path}")
def list_Inflacion():
  return GetInflacion()


@bp.post(f"{path}")
def PostInflacion():
  return SaveInflacion()

@bp.get(f"{path}/prediccion")
def pre_inflacion():
  return prediccion_inflacion()
