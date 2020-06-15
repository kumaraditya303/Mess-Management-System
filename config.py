import os


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    OAUTHLIB_INSECURE_TRANSPORT = '1'
    OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get(
        'MAIL_USERNAME') or 'messmgmtsystem@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'pythonflask'
    CLIENT_ID = (
        '51928570069-otrtlen7ja6duijpl1g1nhuf3201d2j0.apps.googleusercontent.com')
    CLIENT_SECRET = 'SXJyM-582YGw2xeNaVczkwSR'
    REDIRECT_URI = 'https://localhost:5000/login/callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
