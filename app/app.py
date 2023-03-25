from flask import Flask, render_template, request, redirect, url_for, Blueprint

bp = Blueprint('app', __name__)
# jkhgehg


@bp.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
