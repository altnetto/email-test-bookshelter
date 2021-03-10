from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import PasswordField, BooleanField, SubmitField
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