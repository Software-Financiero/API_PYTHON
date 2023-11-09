from flask import Blueprint, request
from src.controllers.microeconomicos.moneda import getMonedaLive, convertMoney, download_initial_data, get_historical_data
from src.controllers.predicciones.moneda import predicciones_moneda
bp = Blueprint("moneda_routes", __name__)


path = '/indicadores/moneda'

@bp.get(f"{path}/live")
def live_moneda():
  return getMonedaLive()

@bp.get(f"{path}/historical")
def h_moneda():
  download_initial_data()
  return get_historical_data()

@bp.post(f"{path}/convert")
def C_moneda():
  amount = request.get_json()['amount']
  print(amount)
  return convertMoney(amount)

@bp.get(f"{path}/prediccion")
def prediccion_moneda():
  return predicciones_moneda()