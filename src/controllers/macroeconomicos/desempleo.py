import pandas as pd
import json
from flask import request


def GetDesempleo():
  return 'Lista Desempleo'

def SaveDesempleo():
  excel_file = request.files['excel']

  xls = pd.read_excel(excel_file, sheet_name="DESEMPLEO", header=None, skiprows=2)
  xls[11] = xls[11].round(2)
  xls = xls.dropna(axis=1, how='any')
  selected_columns = xls[[0, 1, 11]]
  selected_columns.columns = ["Ano", "Mes", "Tasa"]
  selected_columns = selected_columns[selected_columns["Ano"] >= 2014]
  desempleo_dict = selected_columns.to_dict(orient='records')
  data_json = json.dumps(desempleo_dict)
  print(data_json)
  return data_json