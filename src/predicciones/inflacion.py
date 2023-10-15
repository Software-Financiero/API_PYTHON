#manipulacion de datos
import requests as rq
import pandas as pd
from datetime import datetime
import json
#modelacion arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm
import pmdarima as pm
#no advertencias
import warnings
warnings.filterwarnings("ignore")

# Descargar los datos
url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/inflacion"
response = rq.get(url)
inflacion_data =response.json()['data']

# Crear el DataFrame
dates = [f"{entry['Ano']} - {entry['MesNumerico']}" for entry in inflacion_data]
date_objects = [datetime.strptime(date, "%Y - %m") for date in dates]
inflacion_tasa = [entry['Porcentaje'] for entry in inflacion_data]
df = pd.DataFrame({'Fecha': date_objects,'Porcentaje': inflacion_tasa})
df = df.sort_values(by='Fecha').dropna()
df['Fecha'] = pd.to_datetime(df['Fecha'])
df.set_index('Fecha', inplace=True)
df = df[df.index.year > 2015]
df.asfreq('M')

# Divide los datos en conjuntos de entrenamiento y prueba
train_size = int(len(df) * 0.9)
train_data = df[:train_size]
test_data = df[train_size:]
test=test_data.copy()

# Ajustar modelo auto-arima MODELO 
arima_model= sm.tsa.SARIMAX(train_data["Porcentaje"], order=(1,1,1), seasonal_order=(2,0,0,12)).fit()
predictions = arima_model.predict(start="2020-01-01", end="2024-01-01", typ="levels").rename("Arima Predicciones_2024")

meses_dict = {
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

predictions_df = pd.DataFrame({'Fecha': predictions.index, 'Porcentaje': predictions})
predictions_df['Porcentaje'] = predictions_df['Porcentaje'].round(1)
predictions_df['Ano'] = predictions_df['Fecha'].dt.year
predictions_df['Mes'] = predictions_df['Fecha'].dt.month.map(meses_dict)
predictions_df['Dia'] = predictions_df['Fecha'].dt.day
xls_inflacion = predictions_df[["Ano", "Mes", "Dia", 'Porcentaje']]
inflacion_dict = xls_inflacion.to_dict(orient="records")
data_json = json.dumps(inflacion_dict)