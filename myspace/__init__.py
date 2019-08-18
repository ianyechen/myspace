#this is the entry point of the myspace folder, the create_app function can be found here

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from myspace.config import Config 
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False,
#                            default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     item = db.relationship('Item', backref='author', lazy=True)
#     video = db.relationship('Video', backref='author', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}','{self.email}','{self.image_file}')"


# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     time_posted = db.Column(db.DateTime, nullable=False,
#                             default=datetime.utcnow)

#     def __repr__(self):
#         return f"Item('{self.title}','{self.content}')"


# class Video(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     url = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


#     def __repr__(self):
#         return f"Video('{self.name}','{self.url}')"

    
def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from myspace.users.routes import users
    from myspace.lists.routes import lists
    from myspace.main.routes import main 
    from myspace.videos.routes import videos

    app.register_blueprint(users)
    app.register_blueprint(lists)
    app.register_blueprint(main)
    app.register_blueprint(videos)
    

    return app