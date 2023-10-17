from flask import Blueprint
from src.controllers.macroeconomicos.deuda import GetDeuda, SaveDeuda
from src.controllers.predicciones.deuda import prediccion_deuda

bp = Blueprint("deuda_routes", __name__)

path = '/indicadores/deuda'

@bp.get(f"{path}")
def list_Deuda():
  return GetDeuda()


@bp.post(f"{path}")
def PostDeuda():
  return SaveDeuda()

@bp.get(f"{path}/prediccion")
def Pre_deuda():
  return prediccion_deuda()
