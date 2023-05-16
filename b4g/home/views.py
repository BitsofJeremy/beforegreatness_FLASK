
# external imports
from flask import Blueprint, render_template, request, \
    redirect, url_for, flash, jsonify

# Logging
import logging
logger = logging.getLogger(__name__)


home = Blueprint('home', __name__)
home.config = {}


@home.record
def record_params(setup_state):
  app = setup_state.app
  home.config = dict([(key, value) for (key, value) in app.config.items()])


# Basic site routes
@home.route('/', methods=['GET'])
def index():
    """ Main page """
    return render_template('index.html')


@home.route('/about', methods=['GET'])
def about():
    """ About Us page """
    return render_template('about.html')


@home.route('/maillist', methods=['POST'])
def maillist_post():
    """ Subscribe to mail list endpoint """
    return render_template('index.html')