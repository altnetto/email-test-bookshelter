from flask import Flask
from models import login_manager, db
from routes.auth import auth as auth_bp
from routes.user import user as user_bp
from routes.book import book as book_bp

def create_app():

    app = Flask(__name__, template_folder='views')
    app.config.from_object('config.DevConfig')

    with app.app_context():

        db.init_app(app)
        login_manager.init_app(app)

        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(book_bp)

        return app