from . import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET','POST'])
def login():

    errors = {}
    
    form = LoginForm()

    if form.validate_on_submit():

        if form.remember.data:
            remember = True
        else:
            remember = False

        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            errors['error'] = 'Credenciais Incorretas'
            flash(message=errors['error'], category='warning')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, form.password.data):
            errors['error'] = 'Credenciais Incorretas'
            flash(message=errors['error'], category='warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data, duration=timedelta(hours=2))
        flash(message='Usuário {0} logado com sucesso'.format(user.email), category='success')
        return redirect(url_for('user.index'))

    return render_template('login.html', title='Login Page', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash(message='Usuário Deslogado', category='info')
    logout_user()
    return redirect(url_for('user.index'))