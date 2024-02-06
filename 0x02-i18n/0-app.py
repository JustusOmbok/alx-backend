#!/usr/bin/env python3
"""Module for flask app.
"""
from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Define index function."""
    return render_template('0-index.html', title='Welcome to Holberton')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
