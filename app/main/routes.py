import os
import random

import requests
from flask import render_template, flash, redirect, url_for, jsonify, session, abort, request, current_app, \
    make_response
from flask_login import login_user, login_required, logout_user, current_user
from modelscope import Tasks, pipeline
from sqlalchemy import func, and_, desc, or_
from werkzeug.utils import secure_filename
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from datetime import datetime, timedelta
from flask import get_flashed_messages


from . import main
from .email import send_email
from .forms import LoginForm, RegistrationForm, TreeForm, ExpertForm, searchForm, CommentForm
from sklearn.feature_extraction.text import TfidfVectorizer
from .. import db
from ..models import User, Post, Comment, Emotion, Audio, Category, Helpful
from werkzeug.security import generate_password_hash
import re
from random import choice
import string
import json

from collections import defaultdict, Counter


@main.route('/', methods=['GET', 'POST'])
def index():
    trees = Post.query.filter_by(hole=True).order_by(Post.timestamp.desc())

    u_blogs = Post.query.filter(Post.author.has(role=False), Post.hole == False). \
        order_by(desc(Post.read_count)).limit(10).all()

    e_blogs = Post.query.filter(Post.author.has(role=True), Post.hole == False). \
        order_by(desc(Post.read_count)).limit(10).all()

    emotions = []

    flash_message = session.pop('flash_message', None)

    for tree in trees:
        emotion = Emotion.query.filter_by(hole_id=tree.id).first()
        if emotion:
            result_dict = json.loads(emotion.output)
            emotion_label = max(result_dict.items(), key=lambda x: x[1])[0]
            emotions.append(emotion_label)
        else:
            emotions.append(None)

    return render_template('index.html', flash_message=flash_message, u_blogs=u_blogs, e_blogs=e_blogs, emotions=emotions, trees=trees)


@main.route('/404', methods=['GET', 'POST'])
def error():
    return render_template('404.html')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@main.route('/anxiety-grief', methods=['GET', 'POST'])
def anxietygrief():
    return render_template('anxiety-grief.html')


@main.route('/ublog', methods=['GET', 'POST'])
@login_required
def ublog():
    # 获取传递过来的邮箱参数
    email = request.args.get('email')

    # 根据邮箱查找对应用户的博客内容
    user = User.query.filter_by(email=email).first()
    if user is None:
        # 处理用户不存在的情况
        flash('User not found.')
        return redirect(url_for('main.index'))

    sform = searchForm()
    search = ''
    if sform.validate_on_submit():
        search = sform.body.data
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_USER_BLOG_PER_PAGE']

    pagination = Post.query.filter(
        and_(
            Post.author_id == user.id,  # 过滤当前用户的博客
            Post.hole == False,
            (
                    Post.title.like('%' + search + '%') |
                    # Post.category.like('%' + search + '%') |
                    Post.keyA.like('%' + search + '%') |
                    Post.keyB.like('%' + search + '%') |
                    Post.keyC.like('%' + search + '%') |
                    Post.keyD.like('%' + search + '%') |
                    Post.keyE.like('%' + search + '%')
            )
        )
    ).order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    blogs = pagination.items

    return render_template('blog.html', blogs=blogs, pagination=pagination, sform=sform)


@main.route('/blog', methods=['GET', 'POST'])
def blog():
    category_name = request.args.get('category')
    sform = searchForm()
    search = ''
    if sform.validate_on_submit():
        search = sform.body.data
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_USER_BLOG_PER_PAGE']

    if category_name:
        pagination = Post.query.filter(
            and_(
                Post.author.has(role=False),
                Post.hole == False,
                (
                        Post.category_id.like('%' + category_name + '%')
                )
            )
        ).order_by(Post.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        pagination = Post.query.filter(
            and_(
                Post.author.has(role=False),
                Post.hole == False,
                (
                        Post.title.like('%' + search + '%') |
                        # Post.category.like('%' + search + '%') |
                        Post.keyA.like('%' + search + '%') |
                        Post.keyB.like('%' + search + '%') |
                        Post.keyC.like('%' + search + '%') |
                        Post.keyD.like('%' + search + '%') |
                        Post.keyE.like('%' + search + '%')
                )
            )
        ).order_by(Post.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    blogs = pagination.items

    return render_template('blog.html', blogs=blogs, pagination=pagination, sform=sform)


# 单独处理评论的路由
@main.route('/comment', methods=['POST'])
@login_required
def comment():
    comment_body = request.form.get('body')  # 获取评论内容
    post_id = request.form.get('post_id')  # 获取评论所属的文章 ID
    post = Post.query.get_or_404(post_id)

    if comment_body and post_id:
        comment = Comment(body=comment_body,
                          post=post,
                          author=current_user._get_current_object(),
                          timestamp=datetime.now())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published')

    # 重新查询评论数据，更新评论展示区域
    updated_comment_count = db.session.query(func.count(Comment.id)).filter_by(post_id=post_id).scalar()
    updated_pagination = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).paginate(
        page=1, per_page=current_app.config['POST_BLOG_PER_PAGE'], error_out=False)
    updated_comments = updated_pagination.items
    return render_template('comment_section.html', comment_count=updated_comment_count, blog=post, pagination=updated_pagination, comments=updated_comments)


@main.route('/blogdetails/<int:id>', methods=['GET', 'POST'])
def blogdetails(id):
    blog = Post.query.get_or_404(id)
    blog.read_count += 1
    # db.session.commit()

    cform = CommentForm()
    comment_count = db.session.query(func.count(Comment.id)).filter_by(post_id=id).scalar()

    # if cform.validate_on_submit():
    #     comment = Comment(body=cform.body.data,
    #                       post=blog,
    #                       author=current_user._get_current_object(),
    #                       timestamp=datetime.now())
    #     db.session.add(comment)
    #     db.session.commit()
    #     flash('Your comment has been published')
    #
    #     return redirect(url_for('.blogdetails', id=blog.id, page=-1, user=current_user))

    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (len(blog.comments) - 1) // \
               current_app.config['POST_BLOG_PER_PAGE'] + 1
    per_page = current_app.config['POST_BLOG_PER_PAGE']

    pagination = Comment.query.filter_by(post_id=id).order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=per_page,
        error_out=False)
    comments = pagination.items

    # comments = blog.comments.order_by(Comment.timestamp.desc())
    author = blog.author
    # return render_template('blog-details.html', blog=blog, comments=comments, author=author)

    # Extract keywords and update the Post model
    posts = Post.query.all()
    # Assuming the stop words file is in app/static/stopWord.txt
    stopwords_file = os.path.join(os.path.dirname(__file__), 'stopWord.txt')

    # Load stop words from the file
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stop_words = file.readlines()
    stop_words = [word.strip() for word in stop_words]

    # Assuming you have a list of posts' titles and bodies
    # Here, posts_titles and posts_bodies are placeholders for your actual data
    posts_titles = [post.title for post in posts if post.title is not None]
    posts_bodies = [post.body for post in posts if post.body is not None]

    # Concatenate titles and bodies for TF-IDF analysis
    text_data = [title + " " + body for title, body in zip(posts_titles, posts_bodies)]

    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)

    # Fit and transform the text data
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)

    # Get feature names (words) from the TF-IDF vectorizer
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Assuming you want to extract top keywords for each post and store them in the Post model
    # This example extracts top 5 keywords and stores them in keyA to keyE fields
    for i, post in enumerate(posts):
        feature_index = tfidf_matrix[i, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])
        sorted_tfidf_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:5]  # Top 5 keywords
        top_keywords = [feature_names[i] for i, score in sorted_tfidf_scores]

        # Store the top keywords in the Post model
        post.keyA = top_keywords[0] if len(top_keywords) > 0 else ''
        post.keyB = top_keywords[1] if len(top_keywords) > 1 else ''
        post.keyC = top_keywords[2] if len(top_keywords) > 2 else ''
        post.keyD = top_keywords[3] if len(top_keywords) > 3 else ''
        post.keyE = top_keywords[4] if len(top_keywords) > 4 else ''

    # Commit changes to the database
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_BLOG_PER_PAGE']

    # pagination = Post.query.filter_by(hole=False).order_by(Post.timestamp.desc()).paginate(
    #     page=page, per_page=per_page, error_out=False)

    blogsPagination = Post.query.filter(Post.author.has(role=True), Post.hole == False).order_by(
        Post.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    blogs = blogsPagination.items

    # Generate recommendations based on keywords
    effective_words = [word for word in blog.title.split() if word not in stop_words]
    effective_words += [word for word in [blog.keyA, blog.keyB, blog.keyC, blog.keyD, blog.keyE] if
                        word not in stop_words]
    recommendations = []
    added_post_ids = set()  # Keep track of added post ids to avoid duplicates
    keyword_counter = Counter()  # Count keyword occurrences for sorting

    for word in effective_words:
        related_posts = Post.query.filter(or_(Post.title.contains(word), Post.keyA == word, Post.keyB == word,
                                              Post.keyC == word, Post.keyD == word, Post.keyE == word)).all()
        for post in related_posts:
            if post.id not in added_post_ids:
                recommendations.append(post)
                added_post_ids.add(post.id)
                keyword_counter[word] += 1  # Count keyword occurrences for this post

    # Sort recommendations based on keyword occurrences and other criteria
    recommendations.sort(key=lambda x: (keyword_counter[x.keyA] + keyword_counter[x.keyB] + keyword_counter[x.keyC] +
                                        keyword_counter[x.keyD] + keyword_counter[x.keyE],
                                        len(set(effective_words) & set([x.keyA, x.keyB, x.keyC, x.keyD, x.keyE]))),
                         reverse=True)

    # Keep only the top four recommendations
    recommendations = recommendations[1:3]
    return render_template('blog-details.html', blog=blog, blogs=blogs, author=author, pagination=pagination,
                           cform=cform, comments=comments, comment_count=comment_count, recommendations=recommendations,)

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # 获取正式用户数量
    formal_users_count = User.query.filter_by(anonymous=False).count()
    # 获取24小时内新增用户数量
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    new_users_count_24h = User.query.filter(User.timestamp >= twenty_four_hours_ago).count()
    overall = [formal_users_count, new_users_count_24h]

    # 获取所有hole为True属性的帖子的浏览量之和
    hole_posts_views_sum = db.session.query(func.sum(Post.read_count)).filter_by(hole=True).scalar()
    # 获取所有hole为True属性且创建时间在24小时内的帖子数量
    hole_posts_count_24h = Post.query.filter(Post.hole == True, Post.timestamp >= twenty_four_hours_ago).count()
    tree_overall = [hole_posts_views_sum, hole_posts_count_24h]

    # 获取所有hole为False属性的帖子的浏览量之和
    blog_hole_posts_views_sum = db.session.query(func.sum(Post.read_count)).filter_by(hole=False).scalar()
    # 获取所有hole为False属性且创建时间在24小时内的帖子数量
    blog_hole_posts_count_24h = Post.query.filter(Post.hole == False, Post.timestamp >= twenty_four_hours_ago).count()
    blog_overall = [blog_hole_posts_views_sum, blog_hole_posts_count_24h]

    # 获取各种情绪类型的数量
    emotion_counts = {}
    for emotion_label in ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'Neutral']:
        emotion_count = Emotion.query.filter_by(type=1, emotion=emotion_label).count()
        emotion_counts[emotion_label] = emotion_count
    textRatio = [
        emotion_counts['Happy'],
        emotion_counts['Angry'],
        emotion_counts['Surprise'],
        emotion_counts['Sad'],
        emotion_counts['Fear'],
        emotion_counts['Neutral']
    ]

    # 获取各种情绪类型的数量（type=2）
    emotion_counts_audio = {}
    for emotion_label in ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear', 'Neutral']:
        emotion_count_audio = Emotion.query.filter_by(type=2, emotion=emotion_label).count()
        emotion_counts_audio[emotion_label] = emotion_count_audio
    audioRatio = [
        emotion_counts_audio['Happy'],
        emotion_counts_audio['Angry'],
        emotion_counts_audio['Surprise'],
        emotion_counts_audio['Sad'],
        emotion_counts_audio['Fear'],
        emotion_counts_audio['Neutral']
    ]

    blogRatio = []
    categories = ['Dating & Relationship', 'Self Esteem Boosters', 'Family Dynamics & Parenting',
                  'Career Growth & Development', 'Stress Management Techniques', 'Mindfulness & Well-being']
    for category_name in categories:
        # 获取类别的 ID
        category = Category.query.filter_by(name=category_name).first()
        if category:
            # 过滤帖子的 hole 属性和类别 ID
            category_count = Post.query.filter(Post.hole == False, Post.category_id == category_name).count()
            blogRatio.append(category_count)
        else:
            # 如果类别不存在，则添加零计数
            blogRatio.append(0)

    # 获取treePosts列表
    treePosts = []
    emotions = Emotion.query.order_by(Emotion.id.desc()).all()
    for emotion in emotions:
        treePost = {}
        treePost['inputType'] = 'Text' if emotion.type == 1 else 'Audio'
        treePost['email'] = emotion.user.email if emotion.user else 'Unknown'
        treePost['postDate'] = emotion.hole.timestamp if emotion.type == 1 and emotion.hole else (
            emotion.audio.timestamp if emotion.type == 2 and emotion.audio else 'Unknown')
        treePost['emotion'] = emotion.emotion
        treePost['content'] = emotion.hole.body if emotion.hole else emotion.audio.input
        treePosts.append(treePost)

    return render_template('dashboard.html', overall=overall, treeOverall=tree_overall, blogOverall=blog_overall,
                           textRatio=textRatio, audioRatio=audioRatio, blogRatio=blogRatio, treePosts=treePosts)


@main.route('/handle_like/<int:id>', methods=['POST'])
@login_required
def handle_like(id):
    # 获取当前用户
    user = current_user

    # 获取当前用户最近一次的情绪记录
    latest_emotion = Emotion.query.filter_by(user_id=user.id).order_by(Emotion.id.desc()).first()

    if latest_emotion:
        emotion_label = latest_emotion.emotion

        print(emotion_label)  # 输出最高得分的情绪标签
        # 将情绪标签写入 Helpful 数据模型
        helpful_info = Helpful(post_id=id,
                               user_id=user.id,
                               emotion=emotion_label,
                               timestamp=datetime.utcnow())
        db.session.add(helpful_info)
        db.session.commit()
        flash('You liked this post and the emotion was recorded.')
    else:
        flash('No emotion record found.')

    # 重定向到原来的页面或其他页面
    return jsonify({'message': 'Task completed successfully'}), 200


@main.route('/blogsidebar', methods=['GET', 'POST'])
def blogsidebar():
    category_name = request.args.get('category')
    sform = searchForm()
    search = ''
    if sform.validate_on_submit():
        search = sform.body.data

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_BLOG_PER_PAGE']
    if category_name:
        pagination = Post.query.filter(
            and_(
                Post.author.has(role=True),
                Post.hole == False,
                (
                        Post.category_id.like('%' + category_name + '%')
                )
            )
        ).order_by(Post.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        # pagination = Post.query.filter_by(hole=False).order_by(Post.timestamp.desc()).paginate(
        #     page=page, per_page=per_page, error_out=False)

        pagination = Post.query.filter(
            and_(
                Post.author.has(role=True),
                Post.hole == False,
                (
                        Post.title.like('%' + search + '%') |
                        # Post.category.like('%' + search + '%') |
                        Post.keyA.like('%' + search + '%') |
                        Post.keyB.like('%' + search + '%') |
                        Post.keyC.like('%' + search + '%') |
                        Post.keyD.like('%' + search + '%') |
                        Post.keyE.like('%' + search + '%')
                )
            )
        ).order_by(Post.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    blogs = pagination.items

    # blogs = Post.query.filter_by(hole=False).order_by(Post.timestamp.desc()).all()



    return render_template('expertsBlogs.html', blogs=blogs, sform=sform, pagination=pagination )


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
            user.status = True  # 设置用户登录状态为True
            current_user.statue = True
            db.session.commit()
            session['flash_message'] = ('success', 'Login successful. Welcome, {}!'.format(user.email))
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if user.email == "2272393014@qq.com":
                    next = url_for('main.dashboard')
                else:
                    next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form, flash_message=get_flashed_messages(with_categories=True))


@main.route('/logout')
@login_required
def logout():
    current_user.status = False  # 设置用户登出状态为False
    current_user.last_seen = datetime.utcnow()  # 更新用户的last_seen时间
    db.session.commit()
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


# @main.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#             and not current_user.confirmed \
#             and request.endpoint[:5] != 'main.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('main.unconfirmed'))


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
@login_required
def personaldetails(email):
    user = User.query.filter_by(email=email).first()
    return render_template('personal-details.html', user=user)


@main.route('/personaldetailsmodify/<email>', methods=['GET', 'POST'])
@login_required
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
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_USER_BLOG_PER_PAGE']

    pagination = Post.query.filter_by(hole=True).order_by(
        Post.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    trees = pagination.items

    emotions = []  # 用于存储每个hole对应的emotion_label

    for tree in trees:
        # 查询对应的emotion_label
        emotion = Emotion.query.filter_by(hole_id=tree.id).first()
        if emotion:
            result_dict = json.loads(emotion.output)
            emotion_label = max(result_dict.items(), key=lambda x: x[1])[0]
            emotions.append(emotion_label)
        else:
            emotions.append(None)  # 如果没有对应的emotion，则添加None
        print(emotions)

    return render_template('services.html', trees=trees, emotions=emotions, pagination=pagination)


@main.route('/audioservices', methods=['GET', 'POST'])
def audioservices():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_USER_BLOG_PER_PAGE']

    pagination = Audio.query.order_by(
        Audio.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    audios = pagination.items

    emotions = []  # 用于存储每个hole对应的emotion_label

    for aud in audios:
        # 查询对应的emotion_label
        emotion = Emotion.query.filter_by(audio_id=aud.id).first()
        if emotion:
            emotions.append(emotion.emotion)
        else:
            emotions.append(None)  # 如果没有对应的emotion，则添加None
        print(emotions)

    return render_template('audioServices.html', audios=audios, emotions=emotions, pagination=pagination)


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
        return jsonify({'text': "emailFormatError", 'returnvalue': 2})


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


@main.route('/send_blog', methods=['GET', 'POST'])
@login_required
def send_blog():
    form = ExpertForm()

    if form.validate_on_submit():
        # 检测敏感词
        sensitive_words_content = check_sensitive_words(form.content.data)
        sensitive_words_title = check_sensitive_words(form.title.data)

        if sensitive_words_content or sensitive_words_title:
            sensitive_words = ", ".join(set(sensitive_words_content + sensitive_words_title))  # 敏感词列表转换为字符串
            flash(f'Your text contains sensitive words: {sensitive_words}. Please modify and try again.', 'error')
            return redirect(url_for('main.send_blog'))  # 返回发送文本页面并显示错误提示
        else:

            t = form.title.data

            cate_id = form.cate_id.data
            cate = Category.query.get(cate_id)
            if not cate:
                flash('There is no such category, please check the number.')

            photo = request.files['photo']
            fname = photo.filename
            upload_folder = current_app.config['UPLOAD_EPOST']
            allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
            fext = fname.rsplit('.', 1)[-1] if '.' in fname else ''
            if fext not in allowed_extensions:
                flash('Please check if its one of png, '
                      'jpg, jpeg and gif')
                return redirect(url_for('.send_blog'))
            target = '{}{}.{}'.format(upload_folder, t, fext)
            photo.save(target)

            epost = Post(title=form.title.data,
                         cover_url='/static/postPhoto/{}.{}'.format(t, fext),
                         hole=False,
                         body=form.content.data,
                         category_id=form.cate_id.data,
                         author=current_user,
                         )
            db.session.add(epost)
            db.session.commit()

            return redirect(url_for('main.blogsidebar'))
    return render_template('send_blog.html', form=form)


# 获取敏感词列表
def load_sensitive_words():
    sensitive_words = set()
    sensitive_words_file = os.path.join(os.path.dirname(__file__), 'sensitiveen.txt')

    # Load stop words from the file
    with open(sensitive_words_file, 'r', encoding='utf-8') as file:
        for line in file:
            print(line)
            word = line.strip()
            if word:
                sensitive_words.add(word)
    return sensitive_words

# 检测文本中是否包含敏感词


def check_sensitive_words(text):
    sensitive_words = load_sensitive_words()
    words_in_text = text.lower().split()  # 将文本转换为小写并分词
    for word in words_in_text:
        if word in sensitive_words:
            return word  # 返回检测到的第一个敏感词
    return None  # 如果没有检测到敏感词则返回 None


@main.route('/sendtreeText', methods=['GET', 'POST'])
@login_required
def sendtreeText():
    form = TreeForm()
    if form.validate_on_submit():
        # 检测敏感词
        sensitive_word = check_sensitive_words(form.body.data)
        if sensitive_word:
            flash(f'Your text contains a sensitive word: {sensitive_word}. Please modify and try again.', 'error')
            return redirect(url_for('main.sendtreeText'))  # 返回发送文本页面并显示错误提示
        # Generate random user information for anonymous author
        else:
            while True:
                anonymous_username = ''.join(choice(string.ascii_letters) for _ in range(10))
                anonymous_email = f"{anonymous_username}@soulharbor.com"

                # Check if the generated email is unique
                existing_user = User.query.filter_by(email=anonymous_email).first()
                if not existing_user:
                    break  # Exit the loop if the email is unique

            avatar_folder = 'app/static/defaultAvatars'
            avatar_files = [file for file in os.listdir(avatar_folder) if file.endswith('.jpg')]
            if avatar_files:
                random_avatar = random.choice(avatar_files)
                anonymous_avatar_url = f"{avatar_folder}{random_avatar}"

            # Create the anonymous author
            anonymous_author = User(email=anonymous_email, anonymous=True, avatar_url=anonymous_avatar_url,
                                    password_hash=current_user.password_hash)
            db.session.add(anonymous_author)
            db.session.commit()

            # Create the post with anonymous author and current user as the author
            post = Post(
                author=current_user,
                anonymous_author=anonymous_author,
                hole=True,
                body=form.body.data,
                title=" "
            )
            db.session.add(post)

            url = current_app.config['TEXT_TO_EMOTION_URL']
            api_key = current_app.config['TEXT_TO_EMOTION_KEY']
            body = form.body.data
            payload = body.encode("utf-8")
            headers = {
                "apikey": api_key
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            status_code = response.status_code
            result = response.text
            if status_code != 200:
                result = '{"Neutral": 1.0}'

            result_dict = json.loads(result)
            # print(type(result_dict), result_dict)
            emotion_label = max(result_dict.items(), key=lambda x: x[1])[0]
            # print(emotion_label, "++++++++++++++++++++++++++++++++++++++++")

            # 创建 Emotion 对象
            emotion = Emotion(
                type=1,  # 文本情绪
                user=current_user,
                hole=post,  # 连接到新创建的博客对象 epost
                output=result,  # 将情绪检测结果写入 output 字段
                emotion=emotion_label
            )

            # 将 Emotion 对象添加到数据库会话中并提交更改
            db.session.add(emotion)
            db.session.commit()

            return redirect(
                url_for('main.sendresponse', emotion_label=emotion_label))  # Redirect to the blog page after submission
    return render_template('treeText.html', form=form)


@main.route('/sendresponse/<emotion_label>', methods=['GET', 'POST'])
def sendresponse(emotion_label):
    # 查询点赞量很大的前六个帖子
    helpful_posts = db.session.query(Helpful.post_id, func.count(Helpful.id).label('helpful_count')). \
        filter_by(emotion=emotion_label).group_by(Helpful.post_id). \
        order_by(func.count(Helpful.id).desc()).limit(6).all()

    # 根据查询结果获取对应的帖子对象并添加到recommendations列表中
    recommendations = []
    for post_id, helpful_count in helpful_posts:
        post = Post.query.get(post_id)
        if post:
            recommendations.append(post)

    # 如果recommendations为空，则返回最新的六个非树洞帖子
    if not recommendations:
        latest_non_hole_posts = Post.query.filter_by(hole=False).order_by(Post.timestamp.desc()).limit(6).all()
        recommendations.extend(latest_non_hole_posts)

    return render_template('AI-response-detail.html', emotion_label=emotion_label, recommendations=recommendations[:6])


@main.route('/sendtreeAudio', methods=['GET', 'POST'])
@login_required
def sendtreeAudio():
    user = current_user
    if request.method == 'POST':
        if 'audio' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['audio']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and file.filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
            # Generate a unique filename using the user's email and current timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}")
            # filename = secure_filename(f"{user.email}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}")

            audio_file_path = os.path.join(current_app.config['AUDIO_UPLOAD_FOLDER'], filename)
            audio_file_path_DB = os.path.join("../static/audio", filename)


            file.save(audio_file_path)
            # convert_to_valid_wav(audio_file_path)
            flash('File uploaded successfully')

            inference_pipeline = pipeline(
                task=Tasks.emotion_recognition,
                model="iic/emotion2vec_base_finetuned"
            )

            rec_result = inference_pipeline(audio_file_path, granularity="utterance", extract_embedding=False)
            # print(rec_result)

            # 定义标签的分类映射关系
            label_mapping = {
                '开心/happy': 'Happy',
                '生气/angry': 'Angry',
                '吃惊/surprised': 'Surprise',
                '难过/sad': 'Sad',
                '恐惧/fearful': 'Fear',
                '厌恶/disgusted': 'Fear',
                '<unk>': 'Neutral',
                '中立/neutral': 'Neutral',
                '其他/other': 'Neutral'
            }

            if isinstance(rec_result, list) and len(rec_result) > 0:
                result_entry = rec_result[0]
                labels = result_entry.get('labels', [])
                scores = result_entry.get('scores', [])

                # Save the audio file path and emotion detection result in the database
                audio = Audio(input=audio_file_path_DB)
                db.session.add(audio)

                # 合并和分类标签
                merged_labels = defaultdict(float)
                for label, score in zip(labels, scores):
                    mapped_label = label_mapping.get(label, 'Unknown')  # 默认未知标签
                    merged_labels[mapped_label] += score
                # print(merged_labels)

                # 获取权重最高的标签
                max_label = max(merged_labels, key=merged_labels.get)
                # print(max_label, "++++++++++++++++++++++++++++++++++++")

                emotion = Emotion(type=2, user=user, audio=audio, output=f"Labels: {labels}, Scores: {scores}",
                                  emotion=max_label)
                db.session.add(emotion)

                db.session.commit()
            #             return redirect(url_for('main.sendresponse', emotion_label=max_label))
            return jsonify({'url': '/sendresponse/' + max_label})
    return render_template('treeAudioNew.html')
