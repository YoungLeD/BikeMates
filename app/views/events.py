from flask import render_template
from flask_login import login_required, current_user

from app import app


@app.route('/events', methods=['GET', 'POST'])
@login_required
def show_events():
    return render_template('event_main.html', user=current_user)
