#!/usr/bin/env python3
""" Create a single / route and an 0-index.html template
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """ Create a single / route """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
