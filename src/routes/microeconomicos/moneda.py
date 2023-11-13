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

@bp.post(f"{path}/convert/<coin>")
def C_moneda(coin):
  amount = request.get_json()['amount']
  return convertMoney(coin,amount)

@bp.get(f"{path}/prediccion/<days>")
def prediccion_moneda(days):
  return predicciones_moneda(days)