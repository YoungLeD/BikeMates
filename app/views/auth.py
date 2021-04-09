from flask import (flash, redirect, request, render_template, url_for)
from flask_login import (current_user, logout_user)

from app import (app, db, login_manager)
from app.forms import (SignInForm, SignUpForm)
from app import models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get_or_404(user_id)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    """Login page view"""
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    form = SignInForm()
    # if form.validate_on_submit():
    #     return redirect(request.args.get('next') or
    #                     url_for('profile', user_id=current_user.id))
    return render_template('sign_in.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return redirect(url_for('sign_in'))
    """Registration page view

            Returns:
                If data correct: redirect to login page.
                    New user records in database
                If data incorrect: template for registration page
                    again with flashing errors"""
    if current_user.is_authenticated:
        return redirect(url_for('profile', user_id=current_user.id))
    form = SignUpForm()
    if form.validate_on_submit():
        if login_exists(form.email.data):
            flash('This email is already used.', category='error')
            return redirect(url_for('sign_up'))
        u = models.User(form.name.data, form.email.data, form.password.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('sign_in'))
    form.flash_errors()
    return render_template('sign_up.html', form=form)


@app.route('/logout')
def logout():
    """Logout view

    Returns:
        Logouts user and redirect to index"""
    logout_user()
    return redirect(url_for('index'))


def login_exists(login):
    if models.User.query.filter_by(email=login).first():
        return True
    return False


def pass_hash_equal(user_to_verify, requested_user):
    return user_to_verify.pass_hash == requested_user.pass_hash


def verify_user(login, password):
    """Verify a pair of User's login and password

    Args:
        login: User's login to verify
        password: User's password to verify
    Returns:
        ID of user that was verified
        Otherwise None, if this pair of login and password doesn't exist"""
    user_to_verify = models.User('', login, password)
    requested_user = models.User.query.filter_by(email=login).first()
    if not (requested_user and
                pass_hash_equal(user_to_verify, requested_user)):
        return None
    return requested_user
