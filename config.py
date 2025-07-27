import os

class Config:
    # Clave secreta para la seguridad de sesiones, formularios y protección CSRF
    # ¡IMPORTANTE!: En producción, usa una variable de entorno como SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_super_segura_para_el_ambiente_de_desarrollo_popcornhour'

    # Configuración de la base de datos PostgreSQL
    # Asegúrate de que 'tu_usuario' y 'tu_contraseña' sean correctos para tu DB.
    # Puedes usar una variable de entorno DATABASE_URL en producción.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://postgres:Proteccion.1@localhost/popcorn_hour_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desactiva el seguimiento de modificaciones para ahorrar recursos