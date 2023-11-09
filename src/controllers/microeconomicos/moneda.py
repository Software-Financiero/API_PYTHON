from decouple import config
import requests, datetime, time, json

historical_data = []  # Lista para almacenar los datos históricos

def getMonedaLive():
        access_key = config('API_KEY_M')
        currencies = 'COP'

        # Hacemos la petición a la API que nos proporcionará la información.
        url = f"http://api.currencylayer.com/live?access_key={access_key}&currencies={currencies}"
        response = requests.get(url)

        data = response.json()

        # Removemos claves innecesarias del JSON.
        del data['privacy']
        del data['terms']

        # Adecuamos el formato de tiempo del JSON.
        timestamp = data['timestamp']
        datetime_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        data['timestamp'] = formatted_datetime

        return data

def convertMoney(amount):

    access_key = config('API_KEY_M')

    # Hacemos la peticion a la api que nos proporcionara la informacion.
    url = f"http://api.currencylayer.com/convert?access_key={access_key}&from=USD&to=COP&amount={amount}"
    response = requests.get(url)

    data = response.json()

    del data['privacy']
    del data['terms']
    del data['info']

    return data 

# Función para descargar datos iniciales
def download_initial_data():
    url = 'https://www.datos.gov.co/resource/32sa-8pi3.json?$query=SELECT%20%60valor%60%2C%20%60unidad%60%2C%20%60vigenciadesde%60%2C%20%60vigenciahasta%60%0AORDER%20BY%20%60unidad%60%20ASC%20NULL%20LAST%2C%20%60vigenciadesde%60%20DESC%20NULL%20FIRST'
    response = requests.get(url)
    historical_data.extend(response.json())

# Función para actualizar datos en segundo plano
def update_data():
    while True:
        url = 'https://www.datos.gov.co/resource/32sa-8pi3.json?$query=SELECT%20%60valor%60%2C%20%60unidad%60%2C%20%60vigenciadesde%60%2C%20%60vigenciahasta%60%0AORDER%20BY%20%60unidad%60%20ASC%20NULL%20LAST%2C%20%60vigenciadesde%60%20DESC%20NULL%20FIRST'
        response = requests.get(url)
        new_data = response.json()

        # Compara los nuevos datos con los existentes y agrega los nuevos datos a la lista
        for item in new_data:
            if item not in historical_data:
                historical_data.append(item)

        time.sleep(1800)  # Espera 30 minutos antes de verificar nuevamente


def get_historical_data():
    
    fecha_limite = datetime.datetime(2020, 1, 1)

    datos_desde_2020 = [item for item in historical_data if datetime.datetime.fromisoformat(item["vigenciadesde"]) >= fecha_limite]

    return json.dumps(datos_desde_2020)  # Retorna los datos históricos en formato JSON

