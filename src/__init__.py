from flask import Flask

app = Flask(__name__)

def init_app(config):
  app.config.from_object(config)
  return app
