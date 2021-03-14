from . import *

user = Blueprint('user',__name__)


@user.route('/')
def index():
    users = User.query.all()
    return render_template('user.html', users=users, title='Main Page')


@user.route('/add', methods=['POST'])
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

    return redirect(url_for('user.index'))


@user.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.index'))


@user.route('/new', methods=['GET', 'POST'])
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

        return redirect(url_for('user.index'))


    return render_template('new.html', title='New User', form=form)