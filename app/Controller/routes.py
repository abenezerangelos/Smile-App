from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sform = SortForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    
    if sform.validate_on_submit():
        print (sform.sort_order.data, type(sform.sort_order.data).__name__)
        sortSelection = int(sform.sort_order.data)
        if sortSelection == 1:
            posts = Post.query.order_by(Post.happiness_level.desc())
        elif sortSelection == 2:
            posts = Post.query.order_by(Post.likes.desc())
        elif sortSelection == 3:
            posts = Post.query.order_by(Post.title.desc())
        else:
            posts = Post.query.order_by(Post.timestamp.desc())
            
    return render_template('index.html', title="Smile Portal", posts=posts, form = sform)

@bp_routes.route('/postsmile', methods=['GET', 'POST'])  
@login_required
def postsmile():
    pform = PostForm()
    if pform.validate_on_submit():
        newPostForm = Post(title = pform.title.data, body = pform.body.data, happiness_level = pform.happiness_level.data, tags = pform.tag.data, user_id = current_user.id)
        db.session.add(newPostForm)
        db.session.commit()
        flash('A new smile post, "' + pform.title.data + '" has been created! ')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = pform)

@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    post.likes = post.likes + 1
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('routes.index'))
