# pylint: disable=not-callable
from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopementConfig(Config):
    DEBUG = True

config = {
    'development': DevelopementConfig  # Usa la ortografía correcta 'development'
}
