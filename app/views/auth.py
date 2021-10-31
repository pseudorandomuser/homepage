from flask import (
    Blueprint,
    request,
    session,
    redirect,
    render_template
)

from app.auth import users

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    if not ((username := request.form.get('username')) and (
            password := request.form.get('password'))):
        return render_template('login.html',
            error='Username and password can not be empty!')

    auth_success, auth_message = users.authenticate_user(username, password)
    if auth_success:
        session['username'] = username
        return redirect('/')

    return render_template('login.html', error=auth_message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')
