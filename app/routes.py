from flask import Blueprint, render_template, redirect, url_for, flash
# No importamos db o los modelos aquí para evitar circular imports con __init__.py,
# ya que db y los modelos ya están disponibles a través del contexto de la app
# y serán usados en funciones específicas que los requieran.

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # En futuras etapas, aquí cargarás las películas reales desde la base de datos.
    # Por ahora, usamos datos de ejemplo para maquetar la interfaz y ver la estética.
    # Usamos placehold.co para generar URLs de imágenes dinámicas.
    sample_movies = [
        {
            'title': 'Crónicas del Tiempo Perdido',
            'description': 'Una aventura épica a través de dimensiones inexploradas, donde el tiempo es un enemigo.',
            'release_year': 2023,
            'poster': 'https://placehold.co/250x375/3498db/ffffff?text=CronoAventura', # Azul vibrante
            'rating': '4.7',
            'genres': ['Fantasía', 'Aventura', 'Ciencia Ficción']
        },
        {
            'title': 'El Susurro del Viento',
            'description': 'Un thriller psicológico donde cada sombra guarda un secreto mortal.',
            'release_year': 2024,
            'poster': 'https://placehold.co/250x375/e74c3c/ffffff?text=VientoSusurrante', # Rojo intenso
            'rating': '4.1',
            'genres': ['Thriller', 'Misterio']
        },
        {
            'title': 'La Melodía Silenciosa',
            'description': 'Una conmovedora historia de amor y superación en el mundo de la música.',
            'release_year': 2022,
            'poster': 'https://placehold.co/250x375/2ecc71/ffffff?text=MelodiaSilenciosa', # Verde esperanza
            'rating': '4.9',
            'genres': ['Drama', 'Romance', 'Música']
        },
        {
            'title': 'Código Enigma',
            'description': 'Un grupo de hackers debe descifrar un código que amenaza la estabilidad global.',
            'release_year': 2023,
            'poster': 'https://placehold.co/250x375/f1c40f/333333?text=CodigoEnigma', # Amarillo brillante
            'rating': '4.3',
            'genres': ['Acción', 'Ciencia Ficción', 'Suspense']
        },
        {
            'title': 'El Último Guardián',
            'description': 'En un futuro distópico, un solitario guardián protege el último vestigio de la humanidad.',
            'release_year': 2025,
            'poster': 'https://placehold.co/250x375/9b59b6/ffffff?text=UltimoGuardian', # Morado profundo
            'rating': '4.6',
            'genres': ['Ciencia Ficción', 'Acción', 'Distopía']
        },
    ]
    return render_template('home.html', movies=sample_movies)