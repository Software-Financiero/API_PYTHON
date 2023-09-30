from config import config
from src import init_app
from src.routes import indicadores

configuration = config['developement']
app = init_app(configuration)

@app.route('/')
def hello_world():
    return 'Hello World'

app.register_blueprint(indicadores.bp)

if __name__ == '__main__':
    app.run()