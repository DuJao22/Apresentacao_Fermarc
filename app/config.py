"""
Configurações do projeto Fermarc
"""
import os
import sys
import secrets
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def validate_config(config_name='development'):
        """Valida configurações de segurança"""
        if config_name == 'production':
            secret_key = os.environ.get('SECRET_KEY')
            
            # Validar SECRET_KEY em produção
            if not secret_key or secret_key == 'dev-secret-key-change-in-production':
                print("\n" + "="*60)
                print("⚠️  AVISO DE SEGURANÇA CRÍTICO!")
                print("="*60)
                print("SECRET_KEY não configurada ou usando valor padrão!")
                print("Isso é EXTREMAMENTE INSEGURO em produção!")
                print("\nConfigure uma SECRET_KEY forte no arquivo .env:")
                print(f"SECRET_KEY={secrets.token_hex(32)}")
                print("="*60 + "\n")
                sys.exit(1)
            
            # Validar DATABASE_URL em produção
            database_url = os.environ.get('DATABASE_URL')
            if not database_url or 'sqlite' in database_url.lower():
                print("\n" + "="*60)
                print("⚠️  AVISO: Banco de dados não configurado corretamente!")
                print("="*60)
                print("Use PostgreSQL em produção, não SQLite!")
                print("Configure DATABASE_URL no arquivo .env")
                print("="*60 + "\n")
    
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    ITEMS_PER_PAGE = 12
    ADMIN_ITEMS_PER_PAGE = 20
    
    TAX_RATE = 0.0
    SHIPPING_RATE = 15.00
    FREE_SHIPPING_THRESHOLD = 200.00
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
    
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', '')
    PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET', '')
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'data.db')
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
