from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt # Importamos db y bcrypt
from app.models import Movie, User # Importamos los modelos necesarios
from app.forms import RegistrationForm, LoginForm # Importamos los formularios
from flask_login import login_user, current_user, logout_user, login_required # Nuevos imports

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

@main.route('/register', methods=['GET', 'POST'])
def register():
    # Si el usuario ya está logueado, redirigir a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role='standard')
        db.session.add(user)
        db.session.commit()
        flash('¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Registro', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está logueado, redirigir a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user) # Función de Flask-Login para iniciar sesión al usuario
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Inicio de sesión fallido. Por favor, verifica tu email y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

@main.route('/logout')
@login_required # Requiere que el usuario esté logueado para acceder
def logout():
    logout_user() # Función de Flask-Login para cerrar sesión al usuario
    flash('Has cerrado tu sesión.', 'info')
    return redirect(url_for('main.home'))

# Puedes añadir más rutas aquí en el futuro (ej. movie_detail, add_movie, etc.)
