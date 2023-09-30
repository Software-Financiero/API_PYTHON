from flask import Blueprint
from src.controllers.indicadores import getPIB, getDesempleo, getDeudaPublica, getIED, getInflacion, getMoneda, getAcciones

bp = Blueprint("routes", __name__)

path = '/api/indicadores'

@bp.get(f"{path}/PIB")
def list_PIB():
  return getPIB()


@bp.get(f"{path}/desempleo")
def list_desempleo():
  return getDesempleo()


@bp.get(f"{path}/deudaPublica")
def list_deudaPublica():
  return getDeudaPublica()


@bp.get(f"{path}/IED")
def list_IED():
  return getIED()


@bp.get(f"{path}/inflacion")
def list_inflacion():
  return getInflacion()


@bp.get(f"{path}/moneda")
def list_moneda():
  return getMoneda()


@bp.get(f"{path}/acciones")
def list_acciones():
  return getAcciones()