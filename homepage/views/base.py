from flask import Blueprint, render_template

app = Blueprint('base', __name__)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/about')
def about() -> str:
    return render_template('about.html')


@app.route('/projects')
def projects() -> str:
    return render_template('about.html')
