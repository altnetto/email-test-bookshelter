from flask import Blueprint
from flask_mail import Mail, Message

mail = Mail()

email = Blueprint('email', __name__)

@email.route('/email')
def send_mail():

    

    msg = Message(
        subject='Testando o envio de e-mail',
        sender = 'Teste <teste@teste.com.br>',
        recipients = ["altnetto@gmail.com"],
        body = "Meu teste de email"
    )

    mail.send(msg)

    return 'E-mail enviado com sucesso'