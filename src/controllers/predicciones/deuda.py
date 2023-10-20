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

def prediccion_deuda(date):
    response = ''
    if date > '2025-01-01':
        response = { "MSG": "Fecha invalida"}
    else:
# Descargar los datos
        url = "https://tamworth-swift-parrot-msbt.2.us-1.fl0.io/api/v1/deuda"
        response = rq.get(url)
        desempleo_data =response.json()['data']

        meses_dict = {
            "Ene": 1,
            "Feb": 2,
            "Mar": 3,
            "Abr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Ago": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dic": 12
        }

# Crear el DataFrame
        dates = [f"{entry['Ano']} - {meses_dict[entry['Mes']]} - {entry['Dia']}" for entry in desempleo_data ]
        date_objects = [datetime.strptime(date, "%Y - %m - %d") for date in dates]
        pib_values = [entry['total'] for entry in desempleo_data ]
        df = pd.DataFrame({'Fecha': date_objects,'total': pib_values})
        df = df.sort_values(by='Fecha')
        df.reset_index(drop=True, inplace=True)
        df.set_index("Fecha", inplace=True)
        df = df.asfreq('M', method="bfill")

# Divide los datos en conjuntos de entrenamiento y prueba
        train_size = int(len(df) * 0.9)
        train_data = df[:train_size]
        test_data = df[train_size:]
        test=test_data.copy()

#MEJOR MODELO . MODELO 2 CON (0,1,4)(1,0,1,12)
#En END va la fecha 
        arima_model= sm.tsa.ARIMA(df["total"], order=(0,1,0), seasonal_order=(0,1,1,12)).fit()
        predictions = arima_model.predict(start="2020-01-31", end=date, typ="levels")


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
        response = json.dumps(deuda_dict)
    return response