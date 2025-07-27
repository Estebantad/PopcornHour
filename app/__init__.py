from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager # Importamos LoginManager
from config import Config
# REMOVIDA: from app.models import User # Esta línea se mueve dentro de load_user

# Inicializa las extensiones de Flask, pero sin vincularlas a una aplicación todavía
db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager() # Inicialización de LoginManager
login_manager.login_view = 'main.login' # Define la ruta de login para redirect si no está logueado
login_manager.login_message_category = 'info' # Define la categoría de mensajes flash para login

@login_manager.user_loader
def load_user(user_id):
    # ¡IMPORTANTE! Importamos User aquí, DENTRO de la función, para evitar la importación circular.
    from app.models import User 
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    # Crea una instancia de la aplicación Flask
    app = Flask(__name__)
    # Carga la configuración desde tu clase Config
    app.config.from_object(config_class)

    # Vincula las extensiones a la instancia de la aplicación
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app) # Vincula LoginManager a la app

    # Importa y registra los Blueprints (módulos de rutas)
    # Lo hacemos aquí al final de la función para evitar importaciones circulares
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Con el contexto de la aplicación, crea todas las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()

    return app