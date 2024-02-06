#!/usr/bin/env python3
"""Module for flask app.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

# Instantiate the Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Instantiate the Babel object
babel = Babel(app)

# Config class for configuring available languages
class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

# Use Config as config for the Flask app
app.config.from_object(Config)

# Define the get_locale function with babel.localeselector decorator
@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Define index function."""
    return render_template('3-index.html', title=_('home_title'), header=_('home_header'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)