from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from .mongo_inst import mongo
from flask_mail import Mail, Message
app = Flask(__name__)


#Configure app from object input and enable CORS
def create_app(config_obj):
    app.config.from_object(config_obj)
    CORS(app)
    mongo.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(application):
    from app.controllers import items_router
    application.register_blueprint(items_router)

# Testing flask mail
# want to do bulk sending via cron
# search thru db to find items to find similar
@app.route('/mail/<ID>')
def send_mail(ID):
    app.config.update(dict(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'seekr.oose@gmail.com',
        MAIL_PASSWORD = 'Seekroose!',
        MAIL_DEFAULT_SENDER = 'seekr.oose@gmail.com'
    ))
    mail = Mail(app)
    msg = Message("Hello", recipients=["xiniga1163@2go-mail.com"])
    
    msg.html = "<b>I am a nigerian prince</b>"
    mail.send(msg)
    return str(ID)
