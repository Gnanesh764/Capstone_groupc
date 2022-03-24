# this file allows contents to be imported for the website 
from flask import Flask


# from flask_pymongo import PyMongo


def create_app():
    app = Flask(__name__)
    app.config[
        'SECRET_KEY'] = 'absgdhcj'  # secret_key is used for authentication purpose especially, for sessions and cookies
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/Information'  # to link our mongo db Banking
    # PyMongo(app)

    from .views import views
    from .routes import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
