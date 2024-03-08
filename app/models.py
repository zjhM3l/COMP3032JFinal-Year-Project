# from . import login_manager
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from flask_login import UserMixin
import time


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    anonymous = db.Column(db.Boolean, default=False)
    role = db.Column(db.Boolean, default=False)  # False: user, True: doc
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    avatar_url = db.Column(db.String(256))
    intro = db.Column(db.Text)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'))
    career = db.relationship('Career', backref='users')
    awards_urls = db.Column(db.ARRAY(db.String(256)))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.time()
        db.session.add(self)


class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    @staticmethod
    def insert_careers():
        careers = ['Career1', 'Career2', 'Career3']  # 自动生成的职业名称列表
        for c in careers:
            career = Career.query.filter_by(name=c).first()
            if career is None:
                career = Career(name=c)
            db.session.add(career)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    heat = db.Column(db.Integer, default=0)  # 标签热度

    @staticmethod
    def insert_categories():
        categories = ['Category1', 'Category2', 'Category3']  # 自动生成的帖子标签类型列表
        for cat in categories:
            category = Category.query.filter_by(name=cat).first()
            if category is None:
                category = Category(name=cat)
            db.session.add(category)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='posts')
    hole = db.Column(db.Boolean, default=False)
    anonymous_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    anonymous_author = db.relationship('User', foreign_keys=[anonymous_author_id])
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='posts')
    cover_url = db.Column(db.String(256))
    read_count = db.Column(db.Integer, default=0)
    emotion = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)