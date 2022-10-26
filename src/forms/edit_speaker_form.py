from flask_wtf import FlaskForm
from wtforms import SubmitField

class EditSpeakerForm(FlaskForm):
    submit = SubmitField(label='Update')