from flask import Flask
from models import login_manager, db
from routes import bp


def create_app():

    app = Flask(__name__, template_folder='views')
    app.config.from_object('config.DevConfig')

    with app.app_context():

        db.init_app(app)
        login_manager.init_app(app)

        app.register_blueprint(bp)

        return app