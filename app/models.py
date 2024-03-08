# from . import login_manager
from flask import current_app
from . import db
from flask_login import UserMixin


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(64))
