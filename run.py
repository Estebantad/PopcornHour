from app import create_app # Importa la función para crear la aplicación

app = create_app() # Crea la instancia de la aplicación Flask

if __name__ == '__main__':
    # Inicia el servidor de desarrollo de Flask
    # debug=True activa el modo de depuración, que recarga la aplicación automáticamente con los cambios
    # port=5000 es el puerto estándar, puedes cambiarlo si necesitas otro
    app.run(debug=True, port=5000)
