from pymongo import MongoClient
from decouple import config

def connection():  
  # Crea una instancia de MongoClient utilizando la URI
  mongo = MongoClient(config('MONGO_URI'))

  # Crea una base de datos en MongoDB
  db = mongo.BD_FINACIERA
  
  return db
