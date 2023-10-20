from flask import Blueprint, request
import datetime
from src.controllers.macroeconomicos.desempleo import GetDesempleo, SaveDesempleo 
from src.controllers.predicciones.desempleo import prediccion_desempleo

bp = Blueprint("desempleo_routes", __name__)

path = '/indicadores/desempleo'

def last_day_of_month(last_date):
    next_month = last_date.replace(day=28) + datetime.timedelta(days=3)
    return next_month - datetime.timedelta(days=next_month.day)

@bp.get(f"{path}/")
def list_Desempleo():
  return GetDesempleo()


@bp.post(f"{path}/")
def PostDesempleo():
  return SaveDesempleo()

@bp.post(f"{path}/prediccion")
def Pre_desempleo():
  response = request.get_json()['date']
  new_date = datetime.date(int(response['year']),int(response['month']),int(response['day']))
  last_date = last_day_of_month(new_date)
  date = last_date.strftime('%Y-%m-%d')
  return prediccion_desempleo(date)
