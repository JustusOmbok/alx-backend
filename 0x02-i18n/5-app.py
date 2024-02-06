#!/usr/bin/env python3
"""Module for flask app.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Config class for configuring available languages.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Instantiate the Flask app
app = Flask(__name__)
app.config.from_object('config')
app.url_map.strict_slashes = False

# Instantiate the Babel object
babel = Babel(app)

# Use Config as config for the Flask app
app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Define get_user function to retrieve user information."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Define a before_request function
    to execute before all other functions.
    """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    # Check if the 'locale' parameter is present in the request arguments
    if 'locale' in request.args:
        # Get the value of the 'locale' parameter
        requested_locale = request.args.get('locale')
        # Check if the requested locale is in the list of supported languages
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    # If the 'locale' parameter is not present or not supported,
    # use default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Define index function."""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
