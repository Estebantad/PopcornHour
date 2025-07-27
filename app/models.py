from app import db # Importa la instancia de SQLAlchemy desde tu __init__.py
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func # Importa func para AVG

# Tabla de asociación para la relación Many-to-Many entre Movie y Genre
movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Aumentamos la longitud a 255 para almacenar hashes de contraseña más largos
    password_hash = db.Column(db.String(255), nullable=False) 
    role = db.Column(db.String(20), default='standard', nullable=False) # 'standard' o 'moderator'

    # Relaciones: Un usuario puede tener muchas calificaciones y muchos comentarios
    ratings = db.relationship('Rating', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    __tablename__ = 'movies' # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)
    trailer_url = db.Column(db.String(255), nullable=True) # URL del tráiler es opcional

    # Relaciones: Una película puede tener muchas calificaciones y muchos comentarios
    ratings = db.relationship('Rating', backref='movie_obj', lazy=True)
    comments = db.relationship('Comment', backref='movie_obj', lazy=True)

    # Relación Many-to-Many con Genre
    # genres_rel es la relación con la tabla de unión
    genres_rel = db.relationship('Genre', secondary=movie_genre, lazy='subquery',
                                 backref=db.backref('movies_in_genre', lazy=True))
    # genres es un association_proxy para acceder directamente a los nombres de los géneros
    genres = association_proxy('genres_rel', 'name')

    @property
    def average_rating(self):
        # Calcula el promedio de las calificaciones si hay alguna
        if self.ratings:
            # Opción más robusta usando SQLAlchemy func.avg
            avg_score = db.session.query(func.avg(Rating.score)).filter(Rating.movie_id == self.id).scalar()
            return round(avg_score, 1) if avg_score is not None else None
        return None # Retorna None si no hay calificaciones

    @property
    def genres_list(self):
        # Retorna una lista de nombres de géneros para usar fácilmente en plantillas
        return [genre.name for genre in self.genres_rel]

    def __repr__(self):
        return f'<Movie {self.title}>'

class Genre(db.Model):
    __tablename__ = 'genres' # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'

class Rating(db.Model):
    __tablename__ = 'ratings' # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False) # Puntuación de la calificación
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Claves foráneas: Relaciona la calificación con un usuario y una película
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # Asegura que un usuario solo pueda calificar una película una vez
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)

    def __repr__(self):
        return f'<Rating {self.score}>'

class Comment(db.Model):
    __tablename__ = 'comments' # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False) # Contenido del comentario
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Claves foráneas: Relaciona el comentario con un usuario y una película
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.content[:20]}...>' # Muestra los primeros 20 caracteres del comentario
