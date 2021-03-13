from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import Length, Email

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        Email()
    ])
    password = PasswordField('Senha', validators=[
        Length(3,6, "O campo deve conter entre 3 e 6 caracteres")
    ])
    remember = BooleanField('Permanecer Conectado')
    submit = SubmitField('Logar')


class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[
        Length(2,150, "O campo deve conter entre 2 e 150 caracteres")
    ])
    email = EmailField('Email', validators=[
        Email()
    ])
    password = PasswordField('Senha', validators=[
        Length(3,6, "O campo deve conter entre 3 e 6 caracteres")
    ])
    photo = StringField('photo')
    submit = SubmitField('Cadastrar')


class BookForm(FlaskForm):
    name = StringField('Nome', validators=[
        Length(2,125, "O campo deve conter entre 2 e 125 caracteres")
    ])
    submit = SubmitField('Adicionar')