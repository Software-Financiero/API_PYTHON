import pandas as pd
import numpy as np
import requests, json 
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import statsmodels.api as sm
from flask import jsonify

def predicciones_moneda(days):
    # Cargar tus datos históricos en un DataFrame de Pandas
    url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/moneda/datos"
    response = requests.get(url)
    moneda_data = response.json()

    df = pd.DataFrame(moneda_data)
    df['vigenciahasta'] = pd.to_datetime(df['vigenciahasta'])
    df.set_index('vigenciahasta', inplace=True)
    df = df.sort_values('vigenciahasta')

    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['valor'].fillna(0, inplace=True)

    # predicciones futuras
    model = ARIMA(df['valor'], order=(1, 4, 2))
    model_fit = model.fit()
    steps = int(days)
    n_steps = steps
    forecast = model_fit.forecast(steps=n_steps)
    pred_dates = pd.date_range(start=df.index[-1], periods=n_steps)
    predictions_dict = {'fechas': pred_dates.strftime('%Y-%m-%d').tolist(), 'predicciones': forecast.tolist()}

    # predicciones
    train_size = int(len(df) * 1.00)
    train_data = df[:train_size]
    test_data = df[train_size:]
    end_date = train_data.index[-1] 
    start_date = train_data.index[1]
    arima_model= sm.tsa.ARIMA(train_data['valor'], order=(0,1,4), seasonal_order=(1,0,1,12)).fit()
    predictions = arima_model.predict(start=start_date, end=end_date, typ="levels")

    result_dict = {
        'fechas': predictions.index.strftime('%Y-%m-%d').tolist(),
        'predicciones': predictions.tolist(),
    }

    # Combina las listas correspondientes usando zip
    for key in result_dict:
        result_dict[key] += predictions_dict[key]

    result_json = json.dumps(result_dict)
    
    return result_json 


def predicciones_moneda2():
    url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/moneda/datos"
    response = requests.get(url)
    moneda_data = response.json()

    df = pd.DataFrame(moneda_data)
    df['vigenciadesde'] = pd.to_datetime(df['vigenciadesde'])
    df.set_index('vigenciadesde', inplace=True)
    df = df.sort_values('vigenciadesde')

    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['valor'].fillna(0, inplace=True)

    train_size = int(len(df) * 1.00)
    train_data = df[:train_size]
    test_data = df[train_size:]
    test=test_data.copy()

    end_date = train_data.index[-1] 


    arima_model= sm.tsa.ARIMA(train_data['valor'], order=(0,1,4), seasonal_order=(1,0,1,12)).fit()
    predictions = arima_model.predict(start="2020-02-01", end=end_date, typ="levels")

    plt.plot(df.index, df['valor'], label='Datos Originales', color='blue')

    # Graficar las predicciones
    plt.plot(predictions, label='Predicciones', color='red')
    plt.title('Predicciones ARIMA')
    plt.xlabel('Fecha')
    plt.ylabel('Valor')
    plt.legend()
    plt.show() 
