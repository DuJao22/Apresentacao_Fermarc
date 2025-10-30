"""
Fermarc E-commerce - Sistema completo de e-commerce
Desenvolvido por João Lion
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Validar configurações de segurança
    from app.config import Config
    Config.validate_config(config_name)
    
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from flask import session
        cart_count = len(session.get('cart', {}))
        return {
            'current_year': datetime.now().year,
            'site_name': 'Fermarc Robótica',
            'developer': 'João Lion',
            'cart_count': cart_count
        }
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
