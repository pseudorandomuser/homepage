from flask import Blueprint

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return {
        'success': False,
        'message': 'unimplemented'
    }
