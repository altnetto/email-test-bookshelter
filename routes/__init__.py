from flask import Blueprint, request, Response, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Profile, db, login_manager, Book
from datetime import timedelta
from dinForms.forms import LoginForm, RegisterForm, BookForm, UserBookForm

bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('user.html', users=users, title='Main Page')


@bp.route('/add', methods=['POST'])
@login_required
def add_new_user(form):
    name = form.name.data
    email = form.email.data
    password = generate_password_hash(form.password.data)
    photo = form.photo.data

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


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def form_new_user():

    form = RegisterForm()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        photo = form.photo.data

        if User.query.filter_by(email=email).first():
            return 'Erro: E-mail já cadastrado!'

        new_user = User(name=name, email=email, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        new_profile = Profile(photo = photo, user_id = new_user.id)

        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for('bp.index'))


    return render_template('new.html', title='New User', form=form)


@bp.route('/login', methods = ['GET','POST'])
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
            return redirect(url_for('bp.login'))

        if not check_password_hash(user.password, form.password.data):
            errors['error'] = 'Credenciais Incorretas'
            flash(message=errors['error'], category='warning')
            return redirect(url_for('bp.login'))

        login_user(user, remember=form.remember.data, duration=timedelta(hours=2))
        flash(message='Usuário {0} logado com sucesso'.format(user.email), category='success')
        return redirect(url_for('bp.index'))

    return render_template('login.html', title='Login Page', form=form)


@bp.route('/logout')
@login_required
def logout():
    flash(message='Usuário Deslogado', category='info')
    logout_user()
    return redirect(url_for('bp.index'))


@bp.route('/user/<int:id>/add-book', methods=["GET", "POST"])
@login_required
def user_add_book(id):
    
    if id == current_user.id:
            
        form = UserBookForm()

        if form.validate_on_submit():

            book = Book.query.get(form.book.data)

            if book not in current_user.books:

                current_user.books.append(book)

                db.session.add(current_user)
                db.session.commit()

                flash(message='O livro {0} foi adicionado com sucesso para o usuário {1}'.format(book.name,current_user.name), category='success')

            else:
                flash(message='O livro {0} já está na sua lista de livros'.format(book.name), category='warning')

        return render_template('user_add_book.html',title="User Add Book", form = form)

    else:

        flash(message='{0} você não possui permissão para acessar os livros desse usuário'.format(current_user.name), category='warning')
        return redirect(url_for('bp.index'))

@bp.route('/books/add', methods=["GET", "POST"])
@login_required
def add_book():

    form = BookForm()

    books = Book.query.all()

    if form.validate_on_submit():

        name = form.name.data

        new_book = Book(name = name)

        db.session.add(new_book)
        db.session.commit()

        flash(message='O livro {} foi adicionado com sucesso'.format(name), category='success')

        return redirect(url_for('bp.add_book'))

    return render_template('add-book.html',title="Add Book", form = form, books=books)
