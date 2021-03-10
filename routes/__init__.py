from flask import Blueprint, request, Response, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Profile, db, login_manager
from datetime import timedelta
from dinForms.forms import LoginForm

bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('user.html', users=users, title='Main Page')


@bp.route('/add', methods=['POST'])
@login_required
def add_new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'))
    photo = request.form.get('photo')

    if User.query.filter_by(email=email).first():
        return 'Erro: E-mail já cadastrado!'

    new_user = User(name=name, email=email, password=password)
    
    db.session.add(new_user)
    db.session.commit()

    new_profile = Profile(photo = photo, user_id = new_user.id)

    db.session.add(new_profile)
    db.session.commit()

    return redirect(url_for('bp.index'))


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('bp.index'))


@bp.route('/new')
@login_required
def form_new_user():
    return render_template('new.html', title='New User')


@bp.route('/login', methods = ['GET','POST'])
def login():

    errors = {}
    
    form = LoginForm()

    if form.validate_on_submit():

        email = request.form.get('email')
        password = request.form.get('password')

        if request.form.get('remember'):
            remember = True
        else:
            remember = False

        # remember = request.form['remember']

        user = User.query.filter_by(email=email).first()

        # flash('email: {0} pass: {1}'.format(user.email, user.password),'message')

        if not user:
            errors['error'] = 'Credenciais Incorretas'
            flash(message=errors['error'], category='warning')
            return redirect(url_for('bp.login'))

        if not check_password_hash(user.password, password):
            errors['error'] = 'Credenciais Incorretas'
            flash(message=errors['error'], category='warning')
            return redirect(url_for('bp.login'))

        login_user(user, remember=remember, duration=timedelta(hours=2))
        flash(message='Usuário {0} logado com sucesso'.format(user.email), category='success')
        return redirect(url_for('bp.index'))

    return render_template('login.html', title='Login Page', form=form)


@bp.route('/logout')
@login_required
def logout():
    flash(message='Usuário Deslogado', category='info')
    logout_user()
    return redirect(url_for('bp.index'))


@bp.route('/users')
@bp.route('/user/<int:id>')
def posts(id=-1):
    titulo = request.args.get('titulo')

    data = dict(
        path = request.path,
        referrer = request.referrer,
        content_type = request.content_type,
        method = request.method,
        titulo = titulo,
        id = id
    )

    return data