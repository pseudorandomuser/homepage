from flask import Blueprint
from app.models.user import User

app = Blueprint('test', __name__, url_prefix='/test')


@app.route('/insert', methods=['GET'])
def insert():
    User(first_name='TestFirstName', last_name='TestLastName', email='test@address.com').save()
    return {}
