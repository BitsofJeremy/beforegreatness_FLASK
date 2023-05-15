# Import the Flask basics
from logging.config import dictConfig
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Define the user DB
db = SQLAlchemy()

# define logging dict
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '{"date": "%(asctime)s", '
                      '"log_level": "%(levelname)s", '
                      '"module": "%(module)s", '
                      '"message": "%(message)s"}'
         }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'app.log',
            'maxBytes': 1024000,
            'backupCount': 3
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': [
            'wsgi',
            'file'
        ]
    }
})

# Define the App
app = Flask(__name__)

# Pull in the config
app.config.from_pyfile('../config.py')

# Setup the app
db.init_app(app)
# Setup Auth
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

#
# DB Module Imports
#
from b4g.database.models import Users


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


# Import the module / component using their blueprints
# Initial frontend views
from b4g.home.views import home
from b4g.auth.views import auth
# Register the Blueprints with the app
app.register_blueprint(home)
app.register_blueprint(auth)


def unauthorized_callback():
    """"  Handle unauthorized sessions better by redirecting to index """
    flash("You have either been logged out "
          "or you are unauthorized. Please Sign In")
    return redirect(url_for('home.index'))


@app.shell_context_processor
def make_shell_context():
    """ For working with Flask Shell """
    return dict(
        db=db,
        Users=Users
    )
