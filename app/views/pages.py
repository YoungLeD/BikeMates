from flask import render_template, request
from flask_login import current_user

from app import app


@app.route('/')
@app.route('/index')
def index():
    """Index page's view

    Returns:
        Rendered template for /index"""
    return render_template('index.html',
                           title='Home',
                           current=current_user)


@app.route('/api_check', methods=['GET', 'POST'])
def api_check():
    return render_template('api_check.html', user=current_user)


@app.route('/about')
def about():
    """About page's view

        Returns:
            Rendered template for /about"""
    return render_template('about.html', title='About', current=current_user)


@app.route('/demo')
def demo():
    """Release page's view

        Returns:
            Rendered template for /demo"""
    return render_template('demo.html', title='demo')
