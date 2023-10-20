from decouple import config
import requests
import datetime 
import json
import pandas as pd

def getMonedaLive():
  access_key = config('API_KEY')
  currencies = 'COP'

  # Hacemos la peticion a la api que nos proporcionara la informacion.
  url = f"http://api.currencylayer.com/live?access_key={access_key}&currencies={currencies}"
  response = requests.get(url)

  data = response.json()

  #removemos claves innecesarias de el json.
  del data['privacy']
  del data['terms']

  #adecuamos el formato de tiempo de el json.
  timestamp = data['timestamp']
  datetime_object = datetime.datetime.fromtimestamp(timestamp)
  formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
  data['timestamp'] = formatted_datetime

  return data


def convertMoney(amount):

  access_key = config('API_KEY')
  
  # Hacemos la peticion a la api que nos proporcionara la informacion.
  url = f"http://api.currencylayer.com/convert?access_key={access_key}&from=USD&to=COP&amount={amount}"
  response = requests.get(url)

  data = response.json()

  del data['privacy']
  del data['terms']
  del data['info']

  return data 



def getMonedaHistorical():
  access_key = config('API_KEY')
  currencies = 'COP'

  start_date = '2020-01-01'
  end_date = datetime.datetime.today().strftime('%Y-%m-%d')

  data = []

  while start_date <= end_date:
    url = f"http://api.currencylayer.com/timeframe?access_key={access_key}&currencies={currencies}&start_date={start_date}&end_date={end_date}"
    response = requests.get(url)

    data_item = response.json()


    data.append(data_item)

    start_date = (datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

  return json.dumps(data)

