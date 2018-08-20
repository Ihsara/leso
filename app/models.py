# -*- coding: utf-8 -*-
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from time import time

from app import app

#import flask components
from flask_login import UserMixin

#import inner method
from app import db
from app import login


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


multiMediaUsed = db.Table('multi_media_used',
    db.Column('article_id', db.Integer, db.ForeignKey('new_post.id'), primary_key=True),
    db.Column('multimedia_id', db.Integer, db.ForeignKey('multi_media.id'), primary_key=True)
)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('new_post.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    comment = db.relationship('Comment', backref='author', lazy='dynamic')

    #Extra parts for customized contents

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def followed_thrown_away_posts(self):
        own = NewPost.query.filter_by(user_id=self.id)
        return own.order_by(NewPost.timestamp.desc())

    def comments_commented(self):
        own = Comemnt.query.filter_by(user_id=self.id)
        return own.order_by(Comment.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Editor(User):
    editor_right = db.Column(db.Integer, default=1)#Remember to switch it back later !!!
    test_posts = db.relationship('NewPost', backref='author', lazy='dynamic')

    def followed_thrown_away_posts(self):
        own = NewPost.query.filter_by(user_id=self.id)
        return own.order_by(NewPost.timestamp.desc())

    def __repr__(self):
        return '<Editor {}>'.format(self.name)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

class NewPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), index=True, unique=True)
    body= db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('articles', lazy=True))
    synopsis = db.Column(db.String(128))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('article', lazy=True))

    mediaused = db.relationship('MultiMedia', secondary=multiMediaUsed, lazy='dynamic',
        backref=db.backref('media', lazy="dynamic"))

    def __repr__(self):
        return '<NewPost {}>'.format(self.body)


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Discussion {}>'.format(self.name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    timestamp =  db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.relationship('Comment', backref='commenter', lazy='dynamic')
    discussion = comment = db.relationship('Discussion', backref='discussion', lazy='dynamic')

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class MultiMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(128))
    source = db.Column(db.Text)
    source_type = db.Column(db.Text)
    data_retrive= db.Column(db.DateTime, index=True)
    link = db.Column(db.Text)

    def __repr__(self):
        return '<Multimedia {}>'.format(self.id)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return '<NewPost {}>'.format(self.name)