from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content') 
    add = SubmitField('Add')
    update = SubmitField('Update')