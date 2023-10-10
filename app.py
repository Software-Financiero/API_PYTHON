from config import config
from src import init_app
from src.routes import indicadores
from flask_cors import CORS

configuration = config['development']  
app = init_app(configuration)
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to my api-python'

app.register_blueprint(indicadores.bp)

if __name__ == '__main__':
    app.run()