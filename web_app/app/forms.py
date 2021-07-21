from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from web_app.app.models import User
from flask import request


#encapsulate each of the forms in one class

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])    #validators argument is to check that field is not empty
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    email = StringField("Correo Electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    password2 = PasswordField("Confirmar Contraseña", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Por favor usa otro nombre de usuario")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email ya esta registrado")

class EditProfileForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    about_me = TextAreaField("Mi información:", validators=[Length(min=0, max=140)])
    submit = SubmitField('Confirmar')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Email ya esta registrado')
                
class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")

class PostTransportistas(FlaskForm):
    origen = StringField("Origen", validators=[DataRequired()])
    destino = StringField("Destino", validators=[DataRequired()])
    equipo = StringField("Equipo Disponible", validators=[DataRequired()])
    precio_total_deseado = StringField("Costo total a cobrar", validators=[DataRequired()])
    precio_por_unidad_deseado = StringField("Costo por tonelada a cobrar")
    descripcion = TextAreaField("Información extra", validators=[Length(min=0, max=140)])
    usar_info_perfil = BooleanField('Usar información de mi perfil')
    contacto = StringField("Contacto preferido")
    submit = SubmitField("Publicar!")

class PostEmbarcadores(FlaskForm):
    origen = StringField("Origen", validators=[DataRequired()])
    destino = StringField("Destino", validators=[DataRequired()])
    equipo_solicitado = StringField("Equipo Solicitado", validators=[DataRequired()])
    carga = StringField("Carga", validators=[DataRequired()])
    precio_total_ofertado = StringField("Total a Pagar", validators=[DataRequired()])
    precio_por_unidad_ofertado = StringField("Precio por Tonelada a Pagar")
    descripcion = TextAreaField("Información extra, permisos necesarios, consideraciones especiales", validators=[Length(min=0, max=140)])
    usar_info_perfil = BooleanField('Usar información de mi perfil')
    contacto = StringField("Forma de contacto")
    submit = SubmitField("Publicar!")



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Recuperar mi contraseña')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Confirmar Nueva Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Recuperar Contraseña')

class SearchForm(FlaskForm):
    q = StringField("Buscar fletes", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


