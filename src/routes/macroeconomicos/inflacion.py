from flask import Blueprint, request
import datetime
from src.controllers.macroeconomicos.inflacion import GetInflacion, SaveInflacion 
from src.controllers.predicciones.inflacion import prediccion_inflacion

bp = Blueprint("inflacion_routes", __name__)

path = '/indicadores/inflacion'

def last_day_of_month(last_date):
    next_month = last_date.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

@bp.get(f"{path}")
def list_Inflacion():
  return GetInflacion()


@bp.post(f"{path}")
def PostInflacion():
  return SaveInflacion()

@bp.post(f"{path}/prediccion")
def pre_inflacion():
  response = request.get_json()['date']
  new_date = datetime.date(int(response['year']),int(response['month']),int(response['day']))
  last_date = last_day_of_month(new_date)
  date = last_date.strftime('%Y-%m-%d')
  return prediccion_inflacion(date)
