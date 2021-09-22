from datetime import datetime
from app import db

class postTags(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    postrelationship = db.relationship('Post')
    tagrelationship = db.relationship('Tag')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    happiness_level = db.Column(db.Integer, default = 3)
    tags = db.relationship('post_tags', secondary = postTags, primaryjoin=(postTags.post_id == id), backref=db.backref('postTags', lazy='dynamic'), lazy='dynamic')
    
    def get_tags(self):
        return self.tags

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(20))
    def __repr__(self):
        return ('id: {} name: {}'.format(self.id, self.name))




