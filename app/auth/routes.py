from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.models import User, Embed
from app.auth import bp
from app.auth.email import auth_email, reset_email
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordForm, NewPasswordForm, DeleteUserForm


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new User and sends verification email"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)

        # Initiliaze some cools videos!
        embed1 = Embed(embed='mFlrc16xjik',
                       name='Ocean stuff, whales, etc.',
                       author=user)

        embed2 = Embed(embed='Zk0W2UvyINM',
                       name='Relaxing nature',
                       author=user)

        db.session.add(embed1)
        db.session.add(embed2)
        db.session.commit()

        token = user.get_email_token()
        auth_email('welcome@flaskframe.com',
                   'Verify Your Account!',
                   user.email,
                   render_template('email/reg_email.html', token=token))
        flash('Thanks! We just sent an email confirmation. ')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log User in on submit LoginForm or valid verification token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    token = request.args.get('token')
    if token:
        user_id = User.verify_email_token(token)
        if user_id is None:
            flash('Something went wrong! Please try logging in.')
            return redirect(url_for('main.index'))
        user = User.query.get(user_id)
        user.set_verify(True)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        if not user.is_verified:
            flash('You need to verify your account')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# TODO Use DELETE instead of POST
@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    """Delete current_user if User password is valid"""
    form = DeleteUserForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            user = User.query.filter_by(id=current_user.id).first()
            db.session.delete(user)
            db.session.commit()
            # Log user out to remove cookie
            logout_user()
            flash('Account deleted.')
            return(redirect(url_for('auth.login')))
        flash('That password does not seem to match')
        return render_template('auth/delete_user.html', form=form)
    return render_template('auth/delete_user.html', form=form)


@bp.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    """Reset User password if token is valid"""
    user_id = User.verify_email_token(token)
    if user_id is None:
        flash('Something went wrong! Please submit another password reset request.')
        return redirect(url_for('main.index'))
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('main.index'))
    form = NewPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/new_password.html', form=form)


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Send password reset link if User email exists"""
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_email_token()
            reset_email('reset@flaskframe.com',
                        'Reset Password',
                        user.email,
                        render_template('email/reset_email.html', token=token))
            flash('Thanks! We just sent a reset link.')
            return redirect(url_for('auth.login'))
        flash('Thanks! We just sent a reset link.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
