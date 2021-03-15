from flask import Blueprint


def init_app(app):
    from app.routes.auth import auth as auth_bp
    from app.routes.book import book as book_bp
    from app.routes.user import user as user_bp
    from app.routes.email import email as email_bp
    from app.routes.email import mail

    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(email_bp)
    mail.init_app(app)