import time

from flask import (
    Blueprint,
    request,
    session,
    redirect,
    render_template
)

from app.models.user import User
from app.auth.users import AuthenticationError, authenticate_user

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    if not ((username := request.form.get('username')) and (
            password := request.form.get('password'))):
        return render_template('login.html',
            error='Username and password can not be empty!')

    try:
        user_object: User = authenticate_user(username, password)
        session.update({'user': user_object})
        return redirect('/')

    except AuthenticationError as error:
        time.sleep(2.0)  # Delay to slow down brute-force attempts
        return render_template('login.html', error=str(error))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')
