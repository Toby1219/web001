from flask import Flask, session, g
from .config import Config
from .model.models import UserAccount, Admin
from datetime import timedelta
from .utils.extension import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(days=30)


    @login_manager.user_loader
    def load_user(user_id):
        user = UserAccount.query.get(int(user_id))
        if user:
            return user
        admin = Admin.query.get(int(user_id))
        if admin:
            return admin

        return None
                            
    from .routes.auth import auth_bp
    from .routes.views import view_bp
    from .routes.admin import admin_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(view_bp, url_prefix='/')
    
    with app.app_context():
        db.create_all()
        Admin().create_admin()
    
    @app.before_request
    def load_logged_user():
        user_id = session.get('user_id')
        role = session.get('role')
        if user_id and role == 'user':
            g.user = UserAccount.query.get(user_id)
        elif user_id and role == 'admin_':
            g.user = Admin.query.get(user_id)
        else:
            return None
    
    return app

#Webone300625415