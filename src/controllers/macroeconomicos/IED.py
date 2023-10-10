import pandas as pd
import json
from flask import request


def GetIED():
  return 'Lista IED'

def SaveIED():
  excel_file = request.files['excel']

  xls = pd.read_excel(excel_file, sheet_name="IED", header=None, skiprows=2)
  xls[["Ano", "Trimestre"]] = xls[0].str.split('-', expand=True)
  xls[13] =xls[13].apply(lambda x: int(x))
  xls = xls.dropna(subset=["Trimestre"])
  xls_IED = xls[["Ano", "Trimestre", 13]]
  xls_IED= xls_IED.rename(columns={13: "Total"})
  diccionario_IED = xls_IED.to_dict(orient='records')
  data_json = json.dumps(diccionario_IED)

  return data_json
