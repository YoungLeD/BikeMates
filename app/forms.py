# -*- coding: utf8 -*-


from flask import flash
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, DateField, \
    TextAreaField, SelectField, FileField
from wtforms.validators import Email, DataRequired, EqualTo, Length, Optional


class BaseForm(FlaskForm):
    """Form with base methods. It's a parent to all forms below"""

    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" %
                      (getattr(self, field).label.text, error))

    def get_errors(self):
        error_data = []
        for field, errors in self.errors.items():
            for error in errors:
                error_data.append((getattr(self, field).label.text, error))
        return error_data


class SignInForm(BaseForm):
    """Form for sign up

    Attributes:
        email: string, must exist
        password: password hidden string, must exist
        remember_me: flag to remember user in session
    """
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SignUpForm(BaseForm):
    """Form for sign up

    Attributes:
        name: string, must exist and be from 4 to 20 symbols
        email: string, must exist and match email rules
        password: password hidden string, must exist, match
            password rules and be from 8 to 30 symbols
        confirm: password hidden string used to confirm
            filled password
        remember_me: flag to remember user in session
    """
    name = StringField('Name', validators=[
        DataRequired(), Length(min=4, max=20)])
    email = StringField('E-mail', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=30),
    ])
    confirm = PasswordField('Repeat Password', validators=[
        DataRequired(), Length(min=8, max=30),
        EqualTo('password', message='Passwords don\'t match')])
    remember_me = BooleanField('remember_me', default=False)

    def __repr__(self):
        return "name: {}\n" \
               "login: {}\n" \
               "email: {}\n" \
               "password: \n" \
               "confirm: {}\n" \
               "remember_me: {}\n" \
            .format(self.name, self.email, self.password,
                    self.confirm, self.remember_me)


class DataEditForm(BaseForm):
    """Form for editing user's main data

    Attributes:
        name: string, must exist and be from 4 to 20 symbols
        email: string, must exist and match email rules
        bdate: date type, birthday date in format DD.MM.YYYY
        about: text type, max length 500 symbols
        gender: enum type with variants: male, female
    """
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=4, max=120)])
    email = StringField('E-mail',
                        validators=[Email(),
                                    DataRequired()])
    bdate = DateField('Date', format='%d.%m.%Y', validators=[Optional(strip_whitespace=True)])
    about = \
        TextAreaField('Text',
                      validators=[Length(min=0, max=500)])
    gender = SelectField('Gender', choices=[('male', 'Мужской'), ('female', 'Женский')])

    def fill_from_user(self, user):
        self.name.data = user.name
        self.email.data = user.email
        self.bdate.data = user.bdate
        self.about.data = user.about
        self.gender.data = user.gender

    def __repr__(self):
        return 'name: {}, email: {}, bday: {}, about: {}'. \
            format(self.name.data, self.email.data,
                   self.bdate.data, self.about.data)


class PassEditForm(BaseForm):
    """Form for editing user's password

    Attributes:
        old_pass: password hidden string, must exist, match
            password rules, match current password and be
            from 8 to 30 symbols
        new_pass: password hidden string, must exist, match
            password rules and be
            from 8 to 30 symbols
        confirm: password hidden string used to confirm
            filled new password
    """
    old_pass = PasswordField('Password', validators=[DataRequired()])
    new_pass = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=30),
    ])
    confirm = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('new_pass', message='Passwords don\'t match')
    ])


class EventSearchForm(BaseForm):
    """Form for search events

    Attributes:
        search: string, max length 500 symbols
    """
    search = StringField('Search', validator=[Length(min=0, max=500)])


class AvatarUploadForm(BaseForm):
    """Form to upload avatar

    Attributes:
        image: file
    """
    image = FileField('Image File')
