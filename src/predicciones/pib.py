import requests as rq
import pandas as pd
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json

# 2. Análisis estadístico
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm



# modelacion arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm

# no advertencias
import warnings
warnings.filterwarnings("ignore")

# Descargar los datos del API
url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/pib"
response = rq.get(url)
data = response.json()
pib_data = data['data']

# Crear un DataFrame directamente con los datos del API
df = pd.DataFrame(pib_data)
df.drop(['_id', '__v'], axis=1, inplace=True)

# Asegurarse de que los datos estén ordenados por año y trimestre
df['Ano'] = pd.to_numeric(df['Ano'])
df = df.sort_values(['Ano', 'Trimestre'])

# Crear un índice de fecha trimestral
df['Fecha'] = pd.to_datetime(df['Ano'].astype(str) + 'Q' + df['Trimestre'].astype(str))
df.set_index('Fecha', inplace=True)
df = df[df.index.year > 2015]
# Eliminar las columnas 'Ano' y 'Trimestre' si ya no son necesarias
df.drop(['Ano', 'Trimestre'], axis=1, inplace=True)
df.asfreq('Q')

#Para datos desde el 2005
#modelo 2 (0,1,0)(0,0,0,4)
#mayor a 2019
#modelo 2 (1,1,0)(0,0,0,4)
#modelo 1 (3,4,0)(0,0,0,4)

train_size = int(len(df) * 0.9)
train_data = df[:train_size]
test_data = df[train_size:]
test=test_data.copy()

arima_model= sm.tsa.SARIMAX(train_data["PIB"], order=(0,1,0), seasonal_order=(0,0,0,4)).fit()
predictions = arima_model.predict(start="2020-01-01", end="2024-04-01", typ="levels").rename("Arima Predicciones_2024")
predictions_df = pd.DataFrame({'Ano': predictions.index.year, 'Trimestre': predictions.index.quarter,'PIB': predictions})
deuda_dict = predictions_df .to_dict(orient="records")
data_json = json.dumps(deuda_dict)
