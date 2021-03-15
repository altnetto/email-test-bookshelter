from flask import Blueprint, request, Response, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Profile, db, login_manager, Book
from datetime import timedelta
from app.dinForms.forms import LoginForm, RegisterForm, BookForm, UserBookForm

book = Blueprint('book', __name__)


@book.route('/user/<int:id>/add-book', methods=["GET", "POST"])
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
        return redirect(url_for('user.index'))

@book.route('/books/add', methods=["GET", "POST"])
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

        return redirect(url_for('book.add_book'))

    return render_template('add-book.html',title="Add Book", form = form, books=books)