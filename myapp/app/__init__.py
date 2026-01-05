from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class='config.Config'):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_class)
    
    db.init_app(app)
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()
    
    return app