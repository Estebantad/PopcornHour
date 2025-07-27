from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, Optional
from app.models import User # Importamos User para las validaciones personalizadas

# Formulario de Registro de Usuario
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    submit = SubmitField('Registrarse')

    # Validaciones personalizadas para asegurar que el usuario y email sean únicos
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige uno diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado. Por favor, elige uno diferente o inicia sesión.')

# Formulario de Inicio de Sesión
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Formulario para Añadir/Editar Películas (uso para Moderadores)
class MovieForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    release_year = IntegerField('Año de Lanzamiento', validators=[DataRequired(), NumberRange(min=1888, message='Año inválido.')])
    poster_url = StringField('URL del Póster', validators=[DataRequired()])
    trailer_url = StringField('URL del Tráiler (opcional)', validators=[Optional()]) # Ahora es opcional
    genres = StringField('Géneros (separados por coma)', validators=[DataRequired()])
    submit = SubmitField('Guardar Película')

# Formulario para Calificar una Película (uso para Usuarios Estándar)
class RatingForm(FlaskForm):
    # SelectField para el score de 1 a 5, con opciones para mostrar
    score = SelectField('Puntuación', choices=[
        ('1', '1 Estrella'),
        ('2', '2 Estrellas'),
        ('3', '3 Estrellas'),
        ('4', '4 Estrellas'),
        ('5', '5 Estrellas')
    ], validators=[DataRequired()], coerce=int) # coerce=int convierte el valor a entero
    submit_rating = SubmitField('Calificar') # Botón para enviar la calificación

# Formulario para Comentar en una Película (uso para Usuarios Estándar)
class CommentForm(FlaskForm):
    content = TextAreaField('Tu Comentario', validators=[DataRequired(), Length(min=5, max=500, message='El comentario debe tener entre 5 y 500 caracteres.')])
    submit_comment = SubmitField('Publicar Comentario') # Botón para enviar el comentario
