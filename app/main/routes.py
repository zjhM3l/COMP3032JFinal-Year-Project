import os

from flask import render_template, flash, redirect, url_for, jsonify, session, abort, request, current_app, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from . import main
from .email import send_email
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Post, Comment
from werkzeug.security import generate_password_hash
import re
import string


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/404', methods=['GET', 'POST'])
def error():
    return render_template('404.html')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/anxiety-grief', methods=['GET', 'POST'])
def anxietygrief():
    return render_template('anxiety-grief.html')


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    blogs = Post.query.filter_by(hole=False).order_by(Post.timestamp.desc()).all()
    return render_template('blog.html', blogs=blogs)


@main.route('/blogdetails/<int:id>', methods=['GET', 'POST'])
def blogdetails(id):
    blog = Post.query.get_or_404(id)
    comments = blog.comments.order_by(Comment.timestamp.desc())
    author = blog.author
    return render_template('blog-details.html', blog=blog, comments=comments, author=author)


@main.route('/blogsidebar', methods=['GET', 'POST'])
def blogsidebar():
    return render_template('expertsBlogs.html')


@main.route('/career-counseling', methods=['GET', 'POST'])
def lcareercounseling():
    return render_template('career-counseling.html')


@main.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')


@main.route('/case-details', methods=['GET', 'POST'])
def casedetails():
    return render_template('case-details.html')


@main.route('/cases1', methods=['GET', 'POST'])
def cases1():
    return render_template('cases-1.html')


@main.route('/cases2', methods=['GET', 'POST'])
def cases2():
    return render_template('cases-2.html')


@main.route('/send_blog', methods=['GET', 'POST'])
def send_blog():
    return render_template('send_blog.html')


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@main.route('/dating-relationship', methods=['GET', 'POST'])
def datingrelationship():
    return render_template('dating-relationship.html')


@main.route('/family-psycology', methods=['GET', 'POST'])
def familypsycology():
    return render_template('family-psycology.html')


@main.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')


@main.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        passw_hash = generate_password_hash(form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            current_user.statue = True
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash('Login successful. Welcome, {}!'.format(user.email), 'success')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    current_user.statue = False
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,

                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        if send_email(user.email, 'SoulHarbor Confirmation', 'confirm', user=user, token=token):
            flash('The email address is not existed or the network is not connected')
        else:
            flash('You can now check your email')
        # flash('Register successfully')   #判断邮件是否成功发送
        return redirect(url_for('main.login'))
        # return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
    else:
        flash('这个确认链接不可用，或已超时')
    current_user.statue = True
    return redirect(url_for('main.index'))


@main.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'main.' \
            and request.endpoint != 'static':
        return redirect(url_for('main.unconfirmed'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    flash('Invalid email, please try it again')
    return render_template('unconfirmed.html')


@main.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户',
               'templates/confirm', current_user, token)
    flash('新确认账户邮件已发送到邮箱，注意查收.')
    return redirect(url_for('main.index'))


@main.route('/make-appointment', methods=['GET', 'POST'])
def makeappointment():
    return render_template('make-appointment.html')


@main.route('/personaldetails/<email>', methods=['GET', 'POST'])
def personaldetails(email):
    user = User.query.filter_by(email=email).first()
    return render_template('personal-details.html', user=user)


@main.route('/personaldetailsmodify/<email>', methods=['GET', 'POST'])
def personaldetailsmodify(email):
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}  # 允许上传的文件类型
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if 'avatar' in request.files:
            file = request.files['avatar']
            fname = file.filename
            fext = fname.rsplit('.', 1)[-1] if '.' in fname else ''
            if file.filename != '':
                filename = secure_filename(file.filename)
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    target = '{}{}.{}'.format(upload_folder, current_user.email, fext)
                    file.save(target)
                    user.avatar_url = '/static/avatars/{}.{}'.format(current_user.email, fext)
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.intro = request.form.get('intro')
        db.session.commit()
        return redirect(url_for('main.personaldetails', email=user.email, user=current_user))
    return render_template('personal-details-modify.html', email=user.email, user=current_user)


@main.route('/pricing-plans', methods=['GET', 'POST'])
def pricingplans():
    return render_template('pricing-plans.html')


@main.route('/product-details', methods=['GET', 'POST'])
def productdetails():
    return render_template('product-details.html')


@main.route('/products', methods=['GET', 'POST'])
def products():
    return render_template('products.html')


@main.route('/self-esteem-issues', methods=['GET', 'POST'])
def selfesteemissues():
    return render_template('self-esteem-issues.html')


@main.route('/services', methods=['GET', 'POST'])
def services():
    return render_template('services.html')


@main.route('/team', methods=['GET', 'POST'])
def team():
    return render_template('team.html')


@main.route('/young-adult-intensive', methods=['GET', 'POST'])
def youngadultintensive():
    return render_template('young-adult-intensive.html')


@main.route('/checkEmail', methods=['GET', 'POST'])
def checkEmail():
    chosen_email = request.form.get('email');
    if re.match(r'^[0-9a-za-z_]{0,19}@[0-9a-za-z]{1,13}\.[com,cn,net]{1,3}$', chosen_email):
        if not User.query.filter_by(email=chosen_email).first():
            return jsonify({'text': 'Email is available', 'returnvalue': 0})
        else:
            return jsonify({'text': 'Sorry, email is already token', 'returnvalue': 1})
    else:
        return jsonify({'text': "emailFormatError" , 'returnvalue': 2})


@main.route("/passwordStrength", methods=['GET', 'POST'])
def passwordStrength():
    passwordGet = request.form.get("password")
    password = list(passwordGet)
    if len(password) == 0 or " " in password:
        return "format_error"
    special = "`~!@#%^&*()_-+=|}{][:;,.><?/\\"
    has_number, has_lower, has_upper, has_special = 0, 0, 0, 0
    for i in range(0, len(password)):
        if ord('0') <= ord(password[i]) <= ord('9'):
            has_number = 1
        if password[i].islower():
            has_lower = 1
        if password[i].isupper():
            has_upper = 1
        if password[i] in special:
            has_special = 1
    strong = str(has_special + has_number + has_lower + has_upper)
    return jsonify({'text': 'this is the password strength', 'returnvalue': strong})


@main.route('/send_message', methods=['POST'])
def send_message():
    return jsonify({'message': 'Please check your email, and click the link'})

@main.route('/send_message2', methods=['POST'])
def send_message2():
    return jsonify({'message': 'Login succeeded!'})



