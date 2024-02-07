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

    # Check if a user is logged in and if their preferred locale is supported
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Check the request headers for the preferred locale
    request_locale = (
        request.accept_languages.best_match(app.config['LANGUAGES'])
        )
    if request_locale:
        return request_locale

    # If no locale is found, use the default locale
    return app.config['BABEL_DEFAULT_LOCALE']


def get_timezone():
    """Determine the best match for supported timezones."""
    # Check if the 'timezone' parameter is present in the request arguments
    if 'timezone' in request.args:
        # Get the value of the 'timezone' parameter
        requested_timezone = request.args.get('timezone')
        try:
            # Validate if the timezone is valid using pytz.timezone
            pytz.timezone(requested_timezone)
            return requested_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Check if a user is logged in and if their preferred timezone is supported
    if g.user and g.user['timezone']:
        try:
            # Validate if the timezone is valid using pytz.timezone
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default to UTC if no valid timezone is found
    return 'UTC'


# Use the babel.timezoneselector decorator to set the timezone for the app
@babel.timezoneselector
def get_timezone():
    """Define the timezone selector function."""
    return get_timezone()


@app.route('/')
def index():
    """Define index function."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
