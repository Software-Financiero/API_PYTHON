from flask import Blueprint, request
from src.controllers.microeconomicos.moneda import getMonedaLive, getMonedaHistorical, convertMoney

bp = Blueprint("moneda_routes", __name__)


path = '/indicadores/moneda'

@bp.get(f"{path}/live")
def live_moneda():
  return getMonedaLive()

@bp.get(f"{path}/historical")
def h_moneda():
  return getMonedaHistorical()

@bp.post(f"{path}/convert")
def C_moneda():
  amount = request.get_json()['amount']
  return convertMoney(amount)
