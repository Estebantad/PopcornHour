from app import db # Importa la instancia de SQLAlchemy desde tu __init__.py
from datetime import datetime # Para registrar la fecha y hora de creacion/modificacion
from flask_login import UserMixin # Nuevo import

# Tabla intermedia para la relación muchos a muchos entre películas y géneros
movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

class User(db.Model, UserMixin): # Modificado para heredar de UserMixin
    __tablename__ = 'users' # Nombre de la tabla en PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True) # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False, index=True) # Correo electrónico único
    password_hash = db.Column(db.String(128), nullable=False) # Hash de la contraseña para seguridad
    role = db.Column(db.String(20), nullable=False, default='standard') # Rol del usuario: 'standard' o 'moderator'

    # Relaciones con otras tablas:
    # Un usuario puede hacer muchas calificaciones
    ratings = db.relationship('Rating', backref='rater', lazy=True, cascade='all, delete-orphan')
    # Un usuario puede escribir muchos comentarios
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username} (Role: {self.role})>'

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True) # Título de la película, indexado para búsquedas
    description = db.Column(db.Text, nullable=True) # Descripción detallada de la película
    release_year = db.Column(db.Integer, nullable=True) # Año de lanzamiento
    poster_url = db.Column(db.String(500), nullable=True) # URL del póster (usaremos placeholders aquí)
    trailer_url = db.Column(db.String(500), nullable=True) # URL opcional del tráiler

    # Relaciones con otras tablas:
    # Una película puede tener muchas calificaciones
    ratings = db.relationship('Rating', backref='movie_rated', lazy=True, cascade='all, delete-orphan')
    # Una película puede tener muchos comentarios
    comments = db.relationship('Comment', backref='movie_commented', lazy=True, cascade='all, delete-orphan')
    # Relación muchos a muchos con Genre
    genres = db.relationship('Genre', secondary=movie_genre, lazy='subquery',
                             backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'<Movie {self.title} ({self.release_year})>'

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True) # Nombre del género (ej. 'Acción', 'Comedia')

    def __repr__(self):
        return f'<Genre {self.name}>'

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False) # Puntuación de la película (ej. de 1 a 5 estrellas)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Fecha y hora de la calificación

    # Claves foráneas para las relaciones:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # Restricción única: un usuario solo puede calificar una película una vez
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)

    def __repr__(self):
        return f'<Rating {self.score} by User {self.user_id} for Movie {self.movie_id}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False) # Contenido del comentario
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Fecha y hora del comentario

    # Claves foráneas para las relaciones:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return f'<Comment by User {self.user_id} on Movie {self.movie_id[:20]}...>' # Muestra un fragmento del comentario
