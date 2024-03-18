import os
basedir = os.path.abspath(os.path.dirname(__file__))
# from jinja2 import Markup, Environment, FileSystemLoader


class Config:
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = '2272393014@qq.com'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '1483511346@qq.com'
    MAIL_PASSWORD = 'rgmbzaclgrbfiafd'
    FLASKY_MAIL_SENDER = '1483511346@qq.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Group4Confirm]'
    SECURITY_EMAIL_SENDER = 'valid_email@my_domain.com'
    FLASK_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASK_ANNOUNCEMENT_PER_PAGE = 2
    FLASKY_COMMENTS_PER_PAGE = 5
    UPLOAD_FOLDER = os.getcwd() + '/app/static/avatars/'
    FLASK_COMMENTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}