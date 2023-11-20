from decouple import config
from flask import jsonify
import requests, json 

def market_list():

  access_key = config('API_KEY_A4')

  url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={access_key}"

  response = requests.get(url)
  data = response.json()

  if not data:
        return jsonify({'msg': 'Dia no bursatil'})

  return data

def remove_numbers_and_spaces(d):
  return {key.replace(key.split('.')[0] + '.', '').strip(): value for key, value in d.items()}

def stock_historical(symbol):

  access_key = config('API_KEY_A5')

  url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={access_key}"
  response = requests.get(url)
  data = response.json()
  start_year = 2020

  if "Meta Data" in data:

    # Crear un nuevo diccionario para almacenar los datos filtrados
    filtered_data = {
        "Meta Data": data["Meta Data"],
        "Monthly Time Series": {}
    }


    # Recorrer los datos mensuales y agregar solo aquellos a partir del año 2000
    for date, values in data["Monthly Time Series"].items():
        year = int(date.split('-')[0])
        if year >= start_year:
            filtered_data["Monthly Time Series"][date] = remove_numbers_and_spaces(values)


    # Convertir el diccionario filtrado de nuevo a JSON
    filtered_json = json.dumps(filtered_data)
  
    return filtered_json
  else: 
      return data

def stock_data(symbol):  
  symbol_to_find = symbol
  combined_info = {}
  symbol_info = None

  access_key = config('API_KEY_A2')

  url_info = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={access_key}"
  
  response_info = requests.get(url_info)
  data_info = response_info.json()
  
  access_key2 = config('API_KEY_A3')
  url_quotes = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={access_key2}"

  response_quotes = requests.get(url_quotes)
  data_quotes = response_quotes.json()

  for item in data_info.get("bestMatches", []):
    if item.get("1. symbol") == symbol_to_find:
        symbol_info = item
        break

    # Verificar si se encontró el símbolo
  if symbol_info:
      # Combinar la información de ambas fuentes si se encontró el símbolo
      combined_info.update(symbol_info)

  combined_info.update(data_quotes)
  combined_info_json = json.dumps(combined_info)
  return combined_info_json