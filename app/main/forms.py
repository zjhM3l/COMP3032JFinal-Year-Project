from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(message='Email Address please')])
    password = PasswordField('', validators=[DataRequired(message='Password please')])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class TreeForm(FlaskForm):
    body = PageDownField('Say something:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExpertForm(FlaskForm):
    photo = FileField('', validators=[DataRequired()])
    title = TextAreaField('', validators=[DataRequired()])
    cate_id = TextAreaField('', validators=[DataRequired()])

    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('')


class searchForm(FlaskForm):
    body = PageDownField('', validators=[DataRequired()])
    submit = SubmitField('')

class CommentForm(FlaskForm):
    body = PageDownField('', validators=[DataRequired()])
    submit = SubmitField('')
