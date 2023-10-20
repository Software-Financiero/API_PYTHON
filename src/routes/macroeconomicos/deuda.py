from flask import Blueprint, request
import datetime
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

@bp.post(f"{path}/prediccion")
def Pre_deuda():
  response = request.get_json()['date']
  new_date = datetime.date(int(response['year']),int(response['month']),int(response['day']))
  format_date = new_date.replace(day=1)
  date = format_date.strftime('%Y-%m-%d')
  return prediccion_deuda(date)
