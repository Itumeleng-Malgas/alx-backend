#!/usr/bin/env python3
""" 0-app.py:  Babel project """

from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


# Config class with LANGUAGES attribute
class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Use Config as config for Flask app
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
