import pandas as pd
import json
from flask import request


def GetDeuda():
  return 'Lista Deuda'

def SaveDeuda():
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
    
  xls = pd.read_excel(excel_file, sheet_name="DEUDA", header=None)
  xls= xls[xls[1] == 2]
  # Convierte la columna 0 en formato datetime
  xls[0] = pd.to_datetime(xls[0])
  xls['Ano'] = xls[0].dt.year
  xls['Mes'] = xls[0].dt.month
  xls['Dia'] = xls[0].dt.day
  xls["Mes"] = xls["Mes"].map(meses)
  xls_deuda= xls[["Ano", "Mes", "Dia",4]]
  xls_deuda = xls_deuda.rename(columns={4: "total"})
  deuda_dict = xls_deuda.to_dict(orient="records")
  data_json = json.dumps(deuda_dict)
  return data_json