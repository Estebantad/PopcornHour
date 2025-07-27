from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps # Para crear decoradores personalizados
from sqlalchemy.orm import joinedload # Para cargar relaciones de forma eficiente
from sqlalchemy.exc import IntegrityError # Para manejar errores de unicidad
import datetime

from app import db, login_manager # Importa db y login_manager de app/__init__.py
from app.models import User, Movie, Genre, Rating, Comment # Importa todos los modelos
from app.forms import RegistrationForm, LoginForm, MovieForm, RatingForm, CommentForm, CommentForm

# Crea un Blueprint llamado 'main'
main = Blueprint('main', __name__)

# Función para cargar un usuario para Flask-Login (requerido)
@login_manager.user_loader
def load_user(user_id):
    # La importación de User se mueve aquí para evitar importaciones circulares.
    return User.query.get(int(user_id))

# Decorador personalizado para requerir rol de moderador
def moderator_required(f):
    @wraps(f)
    @login_required # Primero asegura que el usuario esté logueado
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'moderator':
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('main.home')) # Redirige a home si no es moderador
        return f(*args, **kwargs)
    return decorated_function

# Ruta de la página de inicio
@main.route('/')
@main.route('/home')
def home():
    # Obtener todas las películas de la base de datos
    # Usamos joinedload para precargar las relaciones genres_rel y ratings para evitar consultas N+1
    movies = Movie.query.options(joinedload(Movie.genres_rel), joinedload(Movie.ratings)).all()

    # Si no hay películas en la DB, mostrar un mensaje apropiado
    if not movies:
        return render_template('home.html', title='Inicio', movies=[], is_empty=True)

    return render_template('home.html', title='Inicio', movies=movies, is_empty=False)


# Ruta de registro de usuario
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # Si ya está logueado, redirige a home
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit(): # Si el formulario es enviado y es válido
        # Quita .decode('utf-8') porque generate_password_hash ya devuelve un string
        hashed_password = generate_password_hash(form.password.data) 
        # Por defecto, todos los usuarios registrados son 'standard'
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role='standard')
        try:
            db.session.add(user)
            db.session.commit()
            flash('¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('main.login')) # Redirige a la página de login
        except IntegrityError:
            db.session.rollback() # Deshacer si hay un error de unicidad (aunque el validador ya lo maneja)
            flash('Error al crear la cuenta. El nombre de usuario o email ya existen.', 'danger')
    return render_template('register.html', title='Registro', form=form)

# Ruta de inicio de sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # Si ya está logueado, redirige a home
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit(): # Si el formulario es enviado y es válido
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user) # Inicia la sesión del usuario
            flash(f'¡Bienvenido de nuevo, {user.username}! Has iniciado sesión. 🎉', 'success')
            # Si el usuario intentó acceder a una página protegida antes de loguearse, redirigirlo allí
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home')) # Redirige a home o a la página solicitada
        else:
            flash('Inicio de sesión fallido. Por favor, verifica tu email y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

# Ruta de cierre de sesión
@main.route('/logout')
@login_required # Requiere que el usuario esté logueado para cerrar sesión
def logout():
    logout_user() # Cierra la sesión del usuario
    flash('Has cerrado tu sesión.', 'info')
    return redirect(url_for('main.home')) # Redirige a home

# Ruta para añadir películas (Solo para Moderadores)
@main.route('/add_movie', methods=['GET', 'POST'])
@moderator_required # Asegura que solo los moderadores logueados puedan acceder
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        new_movie = Movie(
            title=form.title.data,
            description=form.description.data,
            release_year=form.release_year.data,
            poster_url=form.poster_url.data,
            trailer_url=form.trailer_url.data
        )
        
        # Procesar los géneros
        genres_input = [g.strip() for g in form.genres.data.split(',')]
        for genre_name in genres_input:
            if genre_name: # Asegurarse de que el nombre del género no esté vacío
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    # Si el género no existe, créalo
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                new_movie.genres_rel.append(genre) # Añadir el género a la película
        
        try:
            db.session.add(new_movie)
            db.session.commit()
            flash(f'Película "{new_movie.title}" añadida exitosamente.', 'success')
            return redirect(url_for('main.movie_detail', movie_id=new_movie.id)) # Redirige a la página de detalle
        except IntegrityError:
            db.session.rollback()
            flash('Error al añadir la película.', 'danger') # Podría ser por un título duplicado si se añadiera validación
            
    return render_template('add_movie.html', title='Añadir Película', form=form)

# Ruta para ver el detalle de una película, calificar y comentar
@main.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    # Carga la película y sus relaciones ratings y comments y authors para acceso eficiente en la plantilla
    movie = Movie.query.options(
        joinedload(Movie.ratings).joinedload(Rating.author),
        joinedload(Movie.comments).joinedload(Comment.author),
        joinedload(Movie.genres_rel)
    ).get_or_404(movie_id)
    
    rating_form = RatingForm()
    comment_form = CommentForm()

    user_has_rated = False
    existing_rating = None
    if current_user.is_authenticated:
        # Verifica si el usuario actual ya ha calificado esta película
        existing_rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
        if existing_rating:
            user_has_rated = True
            # Pre-rellena el formulario de calificación con la puntuación existente
            rating_form.score.data = existing_rating.score


    return render_template('movie_detail.html',
                           title=movie.title,
                           movie=movie,
                           rating_form=rating_form,
                           comment_form=comment_form,
                           user_has_rated=user_has_rated,
                           existing_rating=existing_rating)

# Ruta para calificar una película
@main.route('/movie/<int:movie_id>/rate', methods=['POST'])
@login_required # Solo usuarios logueados pueden calificar
def rate_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = RatingForm()
    if form.validate_on_submit():
        # Verifica si el usuario ya ha calificado esta película
        existing_rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
        if existing_rating:
            # Actualiza la calificación existente
            existing_rating.score = form.score.data
            flash('Tu calificación ha sido actualizada.', 'success')
        else:
            # Crea una nueva calificación
            new_rating = Rating(score=form.score.data, user_id=current_user.id, movie_id=movie.id)
            db.session.add(new_rating)
            flash('¡Gracias por tu calificación!', 'success')
        
        try:
            db.session.commit()
        except IntegrityError: # Poco probable si el UniqueConstraint funciona, pero buena práctica
            db.session.rollback()
            flash('Ya calificaste esta película.', 'danger')
            
    else: # Si el formulario no es válido
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en {form[field].label.text}: {error}', 'danger')
    return redirect(url_for('main.movie_detail', movie_id=movie.id))

# Ruta para añadir un comentario a una película
@main.route('/movie/<int:movie_id>/comment', methods=['POST'])
@login_required # Solo usuarios logueados pueden comentar
def add_comment(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, user_id=current_user.id, movie_id=movie.id)
        db.session.add(new_comment)
        
        try:
            db.session.commit()
            flash('Tu comentario ha sido publicado exitosamente.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error al publicar el comentario.', 'danger')
    else: # Si el formulario no es válido
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en {form[field].label.text}: {error}', 'danger')
    return redirect(url_for('main.movie_detail', movie_id=movie.id))
