from flask import Blueprint
from src.controllers.macroeconomicos.desempleo import GetDesempleo, SaveDesempleo 

bp = Blueprint("desempleo_routes", __name__)

path = '/indicadores'

@bp.get(f"{path}/desempleo")
def list_Desempleo():
  return GetDesempleo()


@bp.post(f"{path}/desempleo")
def PostDesempleo():
  return SaveDesempleo()
