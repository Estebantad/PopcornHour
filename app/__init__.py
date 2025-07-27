from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from config import Config

# Inicializa las extensiones de Flask, pero sin vincularlas a una aplicación todavía
# Esto permite crear la aplicación en una función (create_app)
db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app(config_class=Config):
    # Crea una instancia de la aplicación Flask
    app = Flask(__name__)
    # Carga la configuración desde tu clase Config
    app.config.from_object(config_class)

    # Vincula las extensiones a la instancia de la aplicación
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    # Importa y registra los Blueprints (módulos de rutas)
    # Lo hacemos aquí al final de la función para evitar importaciones circulares
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Con el contexto de la aplicación, crea todas las tablas de la base de datos si no existen
    # Esto se ejecutará la primera vez que inicies la aplicación
    with app.app_context():
        db.create_all()

    return app
