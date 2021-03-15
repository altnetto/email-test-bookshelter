from flask_mail import Mail, Message
from flask import Blueprint, render_template, flash
from app.dinForms.forms import EmailForm

mail = Mail()

email = Blueprint('email', __name__)

@email.route('/email', methods=["GET", "POST"])
def send_mail():

    form = EmailForm()

    if form.validate_on_submit():

        msg = Message(
            subject='Testando o envio de e-mail',
            sender = '{0} <{1}>'.format(form.name.data, form.email.data),
            recipients = ['madalyn.okuneva@ethereal.email'],
            body = form.message.data
        )

        mail.send(msg)
        flash(message="E-mail enviado com sucesso para {}".format(form.email.data), category='success')

    return render_template('email.html', form=form)