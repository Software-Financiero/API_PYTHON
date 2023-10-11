import pandas as pd
import json
from flask import request


def GetPIB():
  return 'Lista PIB'

def SavePIB():
  excel_file = request.data

  xls = pd.read_excel(excel_file, sheet_name="PIB", header=None, skiprows=2, names=["Periodo", "PIB", "FormaciónBrutaCapital", "Exportaciones", "Importaciones"])
  trimestre_mapping = {"I": 1, "II": 2, "III": 3, "IV": 4}
  xls[["Ano", "Trimestre"]] = xls["Periodo"].str.split('-', expand=True)
  xls["PIB"] = xls["PIB"].apply(lambda x: int(x))
  xls["Trimestre"] = xls["Trimestre"].str.strip().str.upper().map(trimestre_mapping)
  xls_pib = xls[["Ano", "Trimestre", "PIB"]]
  diccionario_pib = xls_pib.to_dict(orient='records')
  data_json = json.dumps(diccionario_pib)
  
  return data_json

  