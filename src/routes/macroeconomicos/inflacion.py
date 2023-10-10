from flask import Blueprint
from src.controllers.macroeconomicos.inflacion import GetInflacion, SaveInflacion 

bp = Blueprint("inflacion_routes", __name__)

path = '/indicadores'

@bp.get(f"{path}/infalcion")
def list_Inflacion():
  return GetInflacion()


@bp.post(f"{path}/inflacion")
def PostInflacion():
  return SaveInflacion()
