import threading
from src.controllers.microeconomicos.moneda import update_data

def update_data():
    threadHistorical = threading.Thread(target=update_data)
    threadHistorical.daemon = True
    threadHistorical.start()

