from flask import (flash, redirect, render_template, request, url_for)
from flask_login import (login_required, current_user)

from app import (app, db, models, login_manager, ALLOWED_EXTENSIONS)
from app.forms import (DataEditForm, PassEditForm, AvatarUploadForm)
import os


@login_manager.user_loader
def load_user(user_id):
    """Loads user with adjusted id

    Args:
        user_id: needed id
    Returns:
        User object with needed id
    """
    return models.User.query.get_or_404(int(user_id))


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def redir_profile():
    """Redirecting user to his own profile if profile's id hasn't
        set in url

    Returns:
        Redirect for profile view with current user's id
    """
    return redirect(url_for('profile', user_id=current_user.id))


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id=None):
    """User's profile page's view

    Args:
        user_id: id of user which profile page we need.
            If None - set current user's id

    Returns:
        Rendered template for user's we need page with remark,
            is he current user
    """
    user = load_user(user_id)
    if user is None:
        return redirect(url_for('index'))
    current = user.id == current_user.id
    return render_template('profile.html',
                           user=user,
                           username=current_user.name,
                           current=current,
                           avatar=user.get_avatar_from_views())


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """User's main data, password and avatar editing view

    Returns:
        Rendered template for current user's account editing page
            with current data for GET-method and with updated data
            after clicking button in this page
    """
    data_form = DataEditForm()
    pass_form = PassEditForm()
    avatar_form = AvatarUploadForm()
    if request.method == 'GET':
        data_form.fill_from_user(current_user)
        return render_template('edit.html',
                               avatar_form=avatar_form,
                               data_form=data_form,
                               pass_form=pass_form,
                               user=current_user,
                               avatar=current_user.get_avatar_from_views())
    if request.method == 'POST':
        data_processing(data_form)
        pass_processing(pass_form)
        avatar_processing()
        return redirect(url_for('edit_profile'))


def avatar_processing():
    """Edit view's helper for changing avatar

    Returns:
        Nothing to return. Helper download file to server and
            set a path to this image for current user after
            clicking appropriate button on edit page if image
            correct
    """
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename.lower()):
            filename = 'id' + current_user.get_id() + '.' \
                       + file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.avatar = filename
            db.session.add(current_user)
            db.session.commit()


def data_processing(data_form):
    """Edit view's helper for updating current user's main data

    Args:
        data_form: input form with fields with main data

    Returns:
        Nothing to return. Helper updating current user's
            main data in database after clicking appropriate
            button on edit page if data correct
    """
    if data_form.validate_on_submit():
        current_user.name = data_form.name.data
        current_user.email = data_form.email.data
        current_user.bdate = data_form.bdate.data
        current_user.about = data_form.about.data
        current_user.gender = data_form.gender.data
        db.session.add(current_user)
        db.session.commit()


def pass_processing(pass_form):
    """Edit view's helper for updating current user's password

    Args:
        pass_form: input form with old and new password

    Returns:
        Nothing to return. Helper updates current user's password
        if input data correct after clicking appropriate button
        on edit page
    """
    if pass_form.validate_on_submit():
        if models.User.hash_password(pass_form.old_pass.data) != \
                current_user.pass_hash:
            return redirect(url_for('edit_profile'))
        current_user.set_password(pass_form.new_pass.data)
        db.session.add(current_user)
        db.session.commit()


def allowed_file(filename):
    """Help spot if uploading file is allowed

    Args:
        filename: uploading file's name with extension

    Returns:
        True if filename allowed or False if filename doesn't allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
