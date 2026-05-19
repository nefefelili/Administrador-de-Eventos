from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

#login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#registracion de roles
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField(
        'Role',
        choices=[('Participante', 'Participante'), ('Organizador', 'Organizador')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

#cambiar password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

#creacion y editacion de eventos
class EventoForm(FlaskForm):
    nombre = StringField('Event Name', validators=[DataRequired()])
    ubicacion = StringField('Location', validators=[DataRequired()])
    fecha_hora = DateTimeLocalField('Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    capacidad = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    descripcion = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')