from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    search = StringField('Search')
    url = StringField('URL')
    add = SubmitField('Add')
    update = SubmitField('Update')