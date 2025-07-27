from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from app.models import User # Importamos el modelo User para validaciones de unicidad

# Formulario de Registro de Usuario
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', 
                           validators=[DataRequired(message="El nombre de usuario es requerido."), 
                                       Length(min=4, max=20, message="El nombre de usuario debe tener entre 4 y 20 caracteres.")])
    email = StringField('Email', 
                        validators=[DataRequired(message="El email es requerido."), 
                                    Email(message="Por favor, introduce un email válido.")])
    password = PasswordField('Contraseña', 
                             validators=[DataRequired(message="La contraseña es requerida."), 
                                         Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[DataRequired(message="Confirma tu contraseña."), 
                                                 EqualTo('password', message='Las contraseñas no coinciden.')])
    submit = SubmitField('Registrarse')

    # Validaciones personalizadas para asegurar que el nombre de usuario y email sean únicos
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige uno diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado. Por favor, elige uno diferente.')

# Formulario de Inicio de Sesión
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(message="El email es requerido."), 
                                    Email(message="Por favor, introduce un email válido.")])
    password = PasswordField('Contraseña', 
                             validators=[DataRequired(message="La contraseña es requerida.")])
    submit = SubmitField('Iniciar Sesión')
