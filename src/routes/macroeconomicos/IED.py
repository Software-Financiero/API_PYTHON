from flask import Blueprint
from src.controllers.macroeconomicos.IED import GetIED, SaveIED 

bp = Blueprint("IED_routes", __name__)

path = '/indicadores'

@bp.get(f"{path}/IED")
def list_IED():
  return GetIED()


@bp.post(f"{path}/IED")
def PostIED():
  return SaveIED()
