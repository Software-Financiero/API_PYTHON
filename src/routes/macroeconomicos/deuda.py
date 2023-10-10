from flask import Blueprint
from src.controllers.macroeconomicos.deuda import GetDeuda, SaveDeuda 

bp = Blueprint("deuda_routes", __name__)

path = '/indicadores'

@bp.get(f"{path}/deuda")
def list_Deuda():
  return GetDeuda()


@bp.post(f"{path}/deuda")
def PostDeuda():
  return SaveDeuda()
