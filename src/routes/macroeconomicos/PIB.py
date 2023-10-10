from flask import Blueprint
from src.controllers.macroeconomicos.PIB import GetPIB, SavePIB 

bp = Blueprint("PIB_routes", __name__)

path = '/indicadores'

@bp.get(f"{path}/PIB")
def list_PIB():
  return GetPIB()


@bp.post(f"{path}/PIB")
def PostPIB():
  return SavePIB()
