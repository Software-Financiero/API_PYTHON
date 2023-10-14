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
url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/desempleo"
response = rq.get(url)
desempleo_data =response.json()['data']

# Crear el DataFrame
dates = [f"{entry['Ano']} - {entry['MesNumerico']}" for entry in desempleo_data]
date_objects = [datetime.strptime(date, "%Y - %m") for date in dates]
desempleo_tasa = [entry['Tasa'] for entry in desempleo_data]
df = pd.DataFrame({'Fecha': date_objects,'Tasa': desempleo_tasa})
df = df.sort_values(by='Fecha').dropna()
df['Fecha'] = pd.to_datetime(df['Fecha'])
df.set_index('Fecha', inplace=True)
df.asfreq('M')

# Divide los datos en conjuntos de entrenamiento y prueba
train_size = int(len(df) * 0.9)
train_data = df[:train_size]
test_data = df[train_size:]
test=test_data.copy()

#MEJOR MODELO . MODELO 2 CON (0,1,4)(1,0,1,12)
#En END va la fecha 
arima_model= sm.tsa.SARIMAX(train_data["Tasa"], order=(0,1,4), seasonal_order=(1,0,1,12)).fit()
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


predictions_df = pd.DataFrame({'Fecha': predictions.index, 'Tasa': predictions})
predictions_df['Tasa'] = predictions_df['Tasa'].round(1)
predictions_df['Ano'] = predictions_df['Fecha'].dt.year
predictions_df['Mes'] = predictions_df['Fecha'].dt.month.map(meses_dict)  # Mapea el número de mes al nombre de mes
predictions_df['Dia'] = predictions_df['Fecha'].dt.day
xls_deuda = predictions_df[["Ano", "Mes", "Dia", 'Tasa']]
deuda_dict = xls_deuda.to_dict(orient="records")
data_json = json.dumps(deuda_dict)

