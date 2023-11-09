import pandas as pd
import numpy as np
import requests
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def predicciones_moneda():
    # Cargar tus datos históricos en un DataFrame de Pandas
    url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/moneda/datos"
    response = requests.get(url)
    moneda_data = response.json()

    df = pd.DataFrame(moneda_data)
    df['vigenciadesde'] = pd.to_datetime(df['vigenciadesde'])
    df.set_index('vigenciadesde', inplace=True)
    df = df.sort_values('vigenciadesde')

    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

    # Lidiar con valores faltantes si es necesario
    # Por ejemplo, para llenar los valores faltantes con ceros:
    df['valor'].fillna(0, inplace=True)

    # Visualizar la serie de tiempo

    data_diff = df['valor'].diff().dropna()

    model = ARIMA(df['valor'], order=(1, 1, 1))
    model_fit = model.fit()

    n_steps = 3

    forecast = model_fit.forecast(steps=n_steps)

    print(forecast) 


    pred_dates = pd.date_range(start=df.index[-1], periods=n_steps)

    plt.figure(figsize=(12, 6))

    # Graficar los datos originales
    plt.plot(df.index, df['valor'], label='Datos Originales', color='blue')

    # Graficar las predicciones
    plt.plot(pred_dates, forecast, label='Predicciones', color='red')

    plt.title('Predicciones ARIMA')
    plt.xlabel('Fecha')
    plt.ylabel('Valor')
    plt.legend()
    plt.show() 

