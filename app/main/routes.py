from flask import render_template, flash, redirect, url_for, session, abort, request, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

