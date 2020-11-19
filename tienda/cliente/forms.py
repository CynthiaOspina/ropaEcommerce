from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Registro

class RegistroCliente(FlaskForm):
    name = StringField('Nombre: ')
    username = StringField('Usuario: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Clave: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Contraseña debe coincidir')])
    confirm = PasswordField('Repetir Clave:', [validators.DataRequired() ])
    country = StringField('País: ', [validators.DataRequired()])
    state = StringField('Provincia: ')
    city = StringField('Ciudad: ', [validators.DataRequired()])
    contact = StringField('Contacto: ', [validators.DataRequired()])
    address = StringField('Direccion: ', [validators.DataRequired()])
    zipcode = StringField('Codigo Postal: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        if Registro.query.filter_by(username=username.data).first():
            raise ValidationError("El usuario ya esta en uso!")

    def validate_email(self, email):
        if Registro.query.filter_by(email=email.data).first():
            raise ValidationError("El email ya esta en uso!")

class LoginClientForm(FlaskForm):
    email = StringField('Email: ', [validators.DataRequired()])
    password = PasswordField('Clave: ', [validators.DataRequired()])
 
class DatosTarjeta(FlaskForm):
    cardholder = StringField('cardholder', [validators.DataRequired()])
    mes = StringField('mes', [validators.DataRequired()])
    anno = StringField('anno', [validators.DataRequired()])
    cardnumber = StringField('carnumber', [validators.DataRequired()])
    ccv = StringField('ccv', [validators.DataRequired()])

