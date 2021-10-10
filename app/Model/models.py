from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

postTags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    happiness_level = db.Column(db.Integer, default = 3)
    tags = db.relationship(
        'Tag', secondary = postTags, 
        primaryjoin=(postTags.c.post_id == id), 
        backref=db.backref('postTags', lazy='dynamic'), lazy='dynamic')
    
    def get_tags(self):
        return self.tags

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(20))
    def __repr__(self):
        return ('id: {} name: {}'.format(self.id, self.name))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return ('id: {} username: {} email: {}'.format(self.id, self.username, self.email))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    


