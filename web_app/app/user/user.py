from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from web_app.app.forms import RegistrationForm, EmptyForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from web_app.app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from web_app.config2 import Config
from web_app.app.user.email_mod import send_password_reset_email
from web_app.app import db



user_bp = Blueprint('user_bp', __name__, template_folder='templates')


@user_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
@user_bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User registered succesfully!")
        return redirect(url_for('auth_bp.login'))
    return render_template('user/register.html', title = "Regístrate", form=form)

@user_bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('user_bp.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user_bp.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()    
    return render_template('user/user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url, form=form) 



@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Cambios guardados satisfactoriamente')
        return redirect(url_for('user_bp.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Editar Perfil', form=form)



@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('main_bp.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user_bp.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('Now you are following {}'.format(username))
        return redirect (url_for('user_bp.user', username=username))
    else:
        return redirect(url_for('main_bp.index'))



@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('main_bp.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user_bp.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You do not follow {} anymore'.format(username))
        return redirect(url_for('user_bp.user', username=username))
    else:
        return redirect(url_for('main_bp.index'))



@user_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash(user.username)
        if user:
            send_password_reset_email(user)
            flash('Check your email for instructions to reset your password')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('No account with that email, try again')
    return render_template('user/reset_password_request.html', title='Restablecer contraseña', form=form)



@user_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main_bp.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been successfully reset')
        return redirect(url_for('auth_bp.login'))
    return render_template('user/reset_password.html', form=form)
