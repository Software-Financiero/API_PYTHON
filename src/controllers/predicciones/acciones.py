import pandas as pd
import numpy as np
import requests, json 
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import statsmodels.api as sm
from src.controllers.microeconomicos.acciones import stock_historical
from flask import jsonify

def predicciones_acciones(symbol):
    # Cargar tus datos históricos en un DataFrame de Pandas
    acciones_data = stock_historical(symbol)
    acciones_dict = json.loads(acciones_data)
    monthly_data = acciones_dict["Monthly Time Series"]
    df = pd.DataFrame(monthly_data).transpose()

    # Convertir índice a tipo de dato datetime
    df.index = pd.to_datetime(df.index)

    # Ordenar el DataFrame por fecha
    df = df.sort_index()

    # Convertir la columna '4. close' a tipo de dato numérico
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    # Rellenar valores nulos en '4. close' con 0
    df['close'].fillna(0, inplace=True)

    # predicciones futuras
    model = ARIMA(df['close'], order=(1, 4, 2))
    model_fit = model.fit()
    n_steps = 5
    forecast = model_fit.forecast(steps=n_steps)
    pred_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(1), periods=n_steps)
    predictions_dict = {'fecha': pred_dates.strftime('%Y-%m-%d').tolist(), 'predicciones': forecast.tolist()}

    # predicciones
    train_size = int(len(df) * 1.00)
    train_data = df[:train_size]
    test_data = df[train_size:]
    end_date = train_data.index[-1]
    start_date = train_data.index[1]
    arima_model= sm.tsa.ARIMA(train_data['close'], order=(0,1,4), seasonal_order=(1,0,1,12)).fit()
    predictions = arima_model.predict(start=start_date, end=end_date, typ="levels")

    result_dict = {
        'fecha': predictions.index.strftime('%Y-%m-%d').tolist(),
        'predicciones': predictions.tolist(),
    }

    # Combina las listas correspondientes usando zip
    for key in result_dict:
        result_dict[key] += predictions_dict[key]

    # Combina las listas correspondientes usando zip
    result_list = [{"fecha": date, "valor": value} for date, value in zip(result_dict['fecha'], result_dict['predicciones'])]
    result_json = json.dumps(result_list)
    
    return result_json 