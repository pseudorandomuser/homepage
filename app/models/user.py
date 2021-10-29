from app.shared.mongodb import mongo


class User(mongo.Document):
    first_name = mongo.StringField()
    last_name = mongo.StringField()
    email = mongo.StringField()
