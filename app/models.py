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
    awards_urls = db.Column(db.String(256))
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
        career1 = Career(id=1, name="career1")
        career2 = Career(id=2, name="career2")
        career3 = Career(id=3, name="career3")
        career4 = Career(id=4, name="career4")
        career5 = Career(id=5, name="career5")
        career6 = Career(id=6, name="career6")
        career7 = Career(id=7, name="career7")
        career8 = Career(id=8, name="career8")
        career9 = Career(id=9, name="career9")
        career10 = Career(id=10, name="career10")
        db.session.add_all([career1, career2, career3, career4, career5, career6, career7,
                            career8, career9, career10])
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    heat = db.Column(db.Integer, default=0)  # 标签热度

    @staticmethod
    def insert_categories():
        category1 = Category(id=1, name="category1")
        category2 = Category(id=2, name="category2")
        category3 = Category(id=3, name="category3")
        category4 = Category(id=4, name="category4")
        category5 = Category(id=5, name="category5")
        category6 = Category(id=6, name="category6")
        db.session.add_all([category1, category2, category3, category4, category5, category6])
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', foreign_keys=[author_id], backref='posts')
    hole = db.Column(db.Boolean, default=False)
    anonymous_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    anonymous_author = db.relationship('User', foreign_keys=[anonymous_author_id], backref='tree_hole')
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='posts')
    cover_url = db.Column(db.String(256))
    read_count = db.Column(db.Integer, default=0)
    emotion = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship('Post', backref='comments')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', foreign_keys=[author_id], backref='comments')
    anonymous_author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    anonymous_author = db.relationship('User', foreign_keys=[anonymous_author_id], backref='anonymous_comments')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
