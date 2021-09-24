from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app.Model.models import Post, Tag

def get_tag():
    return Tag.query.all()

def get_taglabel(tag):
    return tag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level', choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    tag = QuerySelectMultipleField('Tag', query_factory= get_tag, get_label=get_taglabel, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Post')
    body = TextAreaField('Post Message', validators=[DataRequired(), Length(max=1500)])

class SortForm(FlaskForm):
    sort_order = SelectField('Sort Order', choices = [(4, 'Date'),(3, 'Title'), (2, '# of likes'), (1, 'Happiness level')])
    submit = SubmitField('Refresh')

