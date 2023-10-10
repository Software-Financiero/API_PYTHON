import pandas as pd
import json
from flask import request


def GetInflacion():
  return 'Lista Inflacion'

def SaveInflacion():
  excel_file = request.files['excel']

  meses = {
      1: "Ene",
      2: "Feb",
      3: "Mar",
      4: "Abr",
      5: "May",
      6: "Jun",
      7: "Jul",
      8: "Ago",
      9: "Sep",
      10: "Oct",
      11: "Nov",
      12: "Dic"
    }
    
  xls = pd.read_excel(excel_file, sheet_name="INFLACION")
  xls_inflacion = xls[["Año", "Mes", "Porcentaje"]]
  xls_inflacion = xls_inflacion.rename(columns={"Año": "Ano"})
  xls_inflacion["Mes"] = xls_inflacion["Mes"].map(meses)
  inflacion_dict = xls_inflacion.to_dict(orient="records")
  data_json = json.dumps(inflacion_dict)
  return data_json