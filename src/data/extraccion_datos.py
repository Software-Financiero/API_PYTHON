import pandas as pd
import json


def extraccion_PIB_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="PIB", header=None, skiprows=2, names=["Periodo", "PIB", "FormaciónBrutaCapital", "Exportaciones", "Importaciones"])
    trimestre_mapping = {"I": 1, "II": 2, "III": 3, "IV": 4}
    xls[["Ano", "Trimestre"]] = xls["Periodo"].str.split('-', expand=True)
    xls["PIB"] = xls["PIB"].apply(lambda x: int(x))
    xls["Trimestre"] = xls["Trimestre"].str.strip().str.upper().map(trimestre_mapping)
    xls_pib = xls[["Ano", "Trimestre", "PIB"]]
    diccionario_pib = xls_pib.to_dict(orient='records')
    data_json = json.dumps(diccionario_pib)
    return data_json


def extraccion_IED_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="IED", header=None, skiprows=2)
    xls[["Ano", "Trimestre"]] = xls[0].str.split('-', expand=True)
    xls[13] =xls[13].apply(lambda x: int(x))
    xls = xls.dropna(subset=["Trimestre"])
    xls_IED = xls[["Ano", "Trimestre", 13]]
    xls_IED= xls_IED.rename(columns={13: "Total"})
    diccionario_IED = xls_IED.to_dict(orient='records')
    data_json = json.dumps(diccionario_IED)
    return data_json

def extraccion_inflacion_excel(ruta):
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
    
    xls = pd.read_excel(ruta, sheet_name="INFLACION")
    xls_inflacion = xls[["Año", "Mes", "Porcentaje"]]
    xls_inflacion = xls_inflacion.rename(columns={"Año": "Ano"})
    xls_inflacion["Mes"] = xls_inflacion["Mes"].map(meses)
    inflacion_dict = xls_inflacion.to_dict(orient="records")
    data_json = json.dumps(inflacion_dict)
    return data_json
    
def extraccion_desempleo_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="DESEMPLEO", header=None, skiprows=2)
    xls[11] = xls[11].round(2)
    xls = xls.dropna(axis=1, how='any')
    selected_columns = xls[[0, 1, 11]]
    selected_columns.columns = ["Ano", "Mes", "Tasa"]
    desempleo_dict = selected_columns.to_dict(orient='records')
    data_json = json.dumps(desempleo_dict)
    return data_json
    
def extraccion_deuda_excel(ruta):
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
    
    xls = pd.read_excel(ruta, sheet_name="DEUDA", header=None)
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