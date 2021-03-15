from flask import Flask
from app.models import login_manager, db

def create_app():

    app = Flask(__name__, template_folder='views')
    app.config.from_object('app.config.DevConfig')

    with app.app_context():

        db.init_app(app)
        login_manager.init_app(app)

        from app import routes
        routes.init_app(app)

        return app