from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask.globals import current_app
from flask_login import current_user, login_user, logout_user, login_required
from web_app.app.forms import PostForm, SearchForm
from web_app.app.models import Post
from werkzeug.urls import url_parse
from web_app.config2 import Config
from web_app.app import db

main_bp = Blueprint('main_bp', __name__, template_folder='templates')



@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Listing is posted now!")
        return redirect(url_for('main_bp.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, Config.POSTS_PER_PAGE, False)   
    #calling a'all' in the last query triggers the execution, we call 'pagination' here instead
    next_url = url_for('main_bp.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.index', page=posts.prev_num) if posts.has_prev else None

    return render_template('main/index.html', title='Home Page', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)




@main_bp.route('/explore')  #is the default method post?
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main_bp.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@main_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()

@main_bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('.explore'))
    page = request.args.get('page', 1, type=int)
    Post.reindex()
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    print(posts, total)
    print(posts, total)
    next_url = url_for('.search', q=g.search_form.q.data, page=page+1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('.search', q=g.search_form.q.data, page=page-1) if page > 1 else None
    return render_template('main/search.html', title = 'Search', posts=posts, next_url=next_url, prev_url=prev_url)
