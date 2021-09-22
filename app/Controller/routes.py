from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all())

@bp_routes.route('/postsmile', methods=['GET', 'POST'])  
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
        newPostForm = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data, tags = pform.tag.data)
        db.session.add(newPostForm)
        db.session.commit()
        flash('A new smile post, "' + pform.title.data + '" has been created! ')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = pform)

@bp_routes.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    post.likes = post.likes + 1
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('routes.index'))
