from flask import render_template, flash, redirect, url_for, session, abort, request, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/404', methods=['GET', 'POST'])
def login():
    return render_template('404.html')


@main.route('/about', methods=['GET', 'POST'])
def error():
    return render_template('about.html')


@main.route('/anxiety-grief', methods=['GET', 'POST'])
def about():
    return render_template('anxiety-grief.html')


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html')


@main.route('/blog-details', methods=['GET', 'POST'])
def login():
    return render_template('blog-details.html')


@main.route('/blog-sidebar', methods=['GET', 'POST'])
def login():
    return render_template('blog-sidebar.html')


@main.route('/career-counseling', methods=['GET', 'POST'])
def login():
    return render_template('career-counseling.html')


@main.route('/cart', methods=['GET', 'POST'])
def login():
    return render_template('cart.html')


@main.route('/case-details', methods=['GET', 'POST'])
def login():
    return render_template('case-details.html')


@main.route('/cases-1', methods=['GET', 'POST'])
def login():
    return render_template('cases-1.html')


@main.route('/cases-2', methods=['GET', 'POST'])
def login():
    return render_template('cases-2.html')


@main.route('/checkout', methods=['GET', 'POST'])
def login():
    return render_template('checkout.html')


@main.route('/contact', methods=['GET', 'POST'])
def login():
    return render_template('contact.html')


@main.route('/dating-relationship', methods=['GET', 'POST'])
def login():
    return render_template('dating-relationship.html')


@main.route('/family-psycology', methods=['GET', 'POST'])
def login():
    return render_template('family-psycology.html')


@main.route('/faq', methods=['GET', 'POST'])
def login():
    return render_template('faq.html')


@main.route('/gallery', methods=['GET', 'POST'])
def login():
    return render_template('gallery.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main.route('/make-appointment', methods=['GET', 'POST'])
def login():
    return render_template('make-appointment.html')


@main.route('/pricing-plans', methods=['GET', 'POST'])
def login():
    return render_template('pricing-plans.html')


@main.route('/product-details', methods=['GET', 'POST'])
def login():
    return render_template('product-details.html')


@main.route('/products', methods=['GET', 'POST'])
def login():
    return render_template('products.html')


@main.route('/self-esteem-issues', methods=['GET', 'POST'])
def login():
    return render_template('self-esteem-issues.html')


@main.route('/services', methods=['GET', 'POST'])
def login():
    return render_template('services.html')


@main.route('/team', methods=['GET', 'POST'])
def login():
    return render_template('team.html')


@main.route('/team-details', methods=['GET', 'POST'])
def login():
    return render_template('team-details.html')


@main.route('/young-adult-intensive', methods=['GET', 'POST'])
def login():
    return render_template('young-adult-intensive.html')