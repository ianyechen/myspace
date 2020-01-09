from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VideoForm(FlaskForm):
    name = StringField('Name (Name that will be used as reference on your videos page)', validators=[DataRequired()])
    search = StringField('Search (Name of the video that you would like to watch)')
    url = StringField('URL (Link of the video that you would like to watch)')
    add = SubmitField('Add')
    update = SubmitField('Update')