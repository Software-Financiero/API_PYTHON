from flask import Blueprint, request
from src.controllers.microeconomicos.acciones import market_list, stock_historical, stock_data
from src.controllers.predicciones.acciones import predicciones_acciones
bp = Blueprint("acciones_routes", __name__)

path = '/indicadores/acciones'

@bp.get(f"{path}")
def market():
  return market_list()

@bp.get(f"{path}/historical/<symbol>")
def historical(symbol):
  return stock_historical(symbol)

@bp.get(f"{path}/info/<symbol>")
def info(symbol):
  return stock_data(symbol)


@bp.get(f"{path}/prediccion/<symbol>")
def prediccion(symbol):
  return predicciones_acciones(symbol)

