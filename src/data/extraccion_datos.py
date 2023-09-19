import pandas as pd


#API_PYTHON\src\data\LibroExcel.xlsx
# debes llamar la funcion y pasar la ruta donde esta el libro excel

def extraccion_PIB_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="PIB", header=None, names=["Periodo", "PIB","FormaciónBrutaCapital", "Exportaciones","Importaciones"])
    xls[["Año", "Trimestre"]] = xls["Periodo"].str.split('-', expand=True)
    xls["PIB"] =xls["PIB"].apply(lambda x: int(x))
    xls_pib = xls[["Año", "Trimestre", "PIB"]]
    diccionario_pib = xls_pib.to_dict(orient='records')
    return diccionario_pib


def extraccion_IED_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="IED", header=None, skiprows=2)
    xls[["Año", "Trimestre"]] = xls[0].str.split('-', expand=True)
    xls[13] =xls[13].apply(lambda x: int(x))
    xls_IED = xls[["Año", "Trimestre", 13]]
    xls_IED= xls_IED.rename(columns={13: "Total"})
    diccionario_IED = xls_IED.to_dict(orient='records')
    print(diccionario_IED)

def extraccion_inflacion_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="INFLACION")
    xls_inflacion = xls[["Año", "Mes", "Porcentaje"]]
    inflacion_dict = xls_inflacion.to_dict(orient="records")
    return inflacion_dict
    
def extraccion_desempleo_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="DESEMPLEO", header=None, skiprows=2)
    xls[11] = xls[11].round(2)
    xls = xls.dropna(axis=1, how='any')
    selected_columns = xls[[0, 1, 11]]
    selected_columns.columns = ["Año", "Mes", "Tasa"]
    desempleo_dict = selected_columns.to_dict(orient='records')
    return desempleo_dict
    
    
def extraccion_deuda_excel(ruta):
    xls = pd.read_excel(ruta, sheet_name="DEUDA", header=None)
    xls= xls[xls[1] == 2]
    # Convierte la columna 0 en formato datetime
    xls[0] = pd.to_datetime(xls[0])
    xls['Año'] = xls[0].dt.year
    xls['Mes'] = xls[0].dt.month
    xls['Dia'] = xls[0].dt.day
    
    xls_deuda= xls[["Año", "Mes", "Dia",4]]
    xls_deuda = xls_deuda.rename(columns={4: "total"})
    deuda_dict = xls_deuda.to_dict(orient="records")
    return deuda_dict