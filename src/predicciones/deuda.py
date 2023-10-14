#manipulacion de datos
import requests as rq
import pandas as pd
from datetime import datetime
import json

#modelacion arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm

#no advertencias
import warnings
warnings.filterwarnings("ignore")

# Descargar los datos
url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/deuda"
response = rq.get(url)
deuda_data = response.json()['data']

# Crear el DataFrame
dates = [f"{entry['Ano']} - {entry['MesNumerico']} - {entry['Dia']}" for entry in deuda_data]
print(dates)
date_objects = [datetime.strptime(date, "%Y - %m - %d") for date in dates]
deuda_values = [entry['total'] for entry in deuda_data]
df = pd.DataFrame({'Fecha': date_objects,'Total': deuda_values})
df = df.sort_values(by='Fecha').dropna()
df['Fecha'] = pd.to_datetime(df['Fecha'])
df.set_index('Fecha', inplace=True)
df.asfreq('M')

# Divide los datos en conjuntos de entrenamiento y prueba
train_size = int(len(df) * 0.9)
train_data = df[:train_size]
test_data = df[train_size:]
test=test_data.copy()

#(0,1,0)(0,1,1,12)
arima_model= sm.tsa.SARIMAX(train_data["Total"], order=(0,1,0), seasonal_order=(0,1,1,12)).fit()
predictions = arima_model.predict(start="2020-01-31", end="2025-01-31", typ="levels").rename("Arima Predicciones_2024")


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

predictions_df = pd.DataFrame({'Fecha': predictions.index, 'total': predictions})
predictions_df['total'] = predictions_df['total'].round(1)
predictions_df['Ano'] = predictions_df['Fecha'].dt.year
predictions_df['Mes'] = predictions_df['Fecha'].dt.month.map(meses_dict)  
predictions_df['Dia'] = predictions_df['Fecha'].dt.day
xls_deuda = predictions_df[["Ano", "Mes", "Dia", 'total']]
deuda_dict = xls_deuda.to_dict(orient="records")
data_json = json.dumps(deuda_dict)

