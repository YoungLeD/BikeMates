# Flask-Login
from flask_login import LoginManager

login_manager = LoginManager()

# Flask-WTF CSRF Protection
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

# Flask-CORS
from flask_cors import CORS

cors = CORS()


# SQLAlchemy
def config(app, config):
    # SECRET
    app.secret_key = config['SECRET_KEY']

    # SQLAlchemy
    app.config.update(config['SQLAlchemy'])

    # JWT
    from datetime import timedelta
    JWT_config = config.get('JWT', {})
    app.config.update(JWT_config)
    JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA = JWT_config.get('JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA', {})
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
        days=JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA.get('days', 0),
        hours=JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA.get('hours', 0),
        minutes=JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA.get('minutes', 15),
        seconds=JWT_ACCESS_TOKEN_EXPIRES_TIMEDELTA.get('seconds', 0)
    )
    JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA = JWT_config.get('JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA', {})
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
        days=JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA.get('days', 30),
        hours=JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA.get('hours', 0),
        minutes=JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA.get('minutes', 0),
        seconds=JWT_REFRESH_TOKEN_EXPIRES_TIMEDELTA.get('seconds', 0)
    )

    # Flask-Login
    login_manager.login_view = config.get('Flask_Login', {}).get('LOGIN_VIEW', '')
    login_manager.init_app(app)

    # Flask-WTF
    csrf.init_app(app)

    # Flask-CORS
    cors.init_app(app)
