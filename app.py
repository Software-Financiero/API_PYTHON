from config import config
from flask_cors import CORS
from src import init_app
from src.routes.macroeconomicos import PIB, IED, deuda, desempleo, inflacion
from src.routes.microeconomicos import moneda, acciones
from src.worker.threands import update_data


configuration = config['development']  
app = init_app(configuration)
CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to my api-python'

app.register_blueprint(PIB.bp)
app.register_blueprint(IED.bp)
app.register_blueprint(inflacion.bp)
app.register_blueprint(desempleo.bp)
app.register_blueprint(deuda.bp)
app.register_blueprint(moneda.bp)
app.register_blueprint(acciones.bp)

if __name__ == '__main__':
    update_data()
    app.run()