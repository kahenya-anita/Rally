from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import db

from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class Quote:
    def __init__(self,author,quote,permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)    
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String)
    prof_pic_path = db.Column(db.String)
    bio = db.Column(db.String)
    password_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'{self.username}'

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String)
    text=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)    
    post_pic_path = db.Column(db.String) 
    comments = db.relationship('Comment',backref = 'post',lazy = "dynamic")  

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.id}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_text=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)    
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.comment}'


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255),unique = True,index = True) 

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.email}'

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),index = True) 
    title = db.Column(db.String)
    message = db.Column(db.String)

    def save_contact(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.title}'



