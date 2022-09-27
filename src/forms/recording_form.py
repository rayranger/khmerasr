from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField

class RecordingForm(FlaskForm):
    sample_file = FileField(label="Sample audio file")
    submit = SubmitField(label="Save new recording")
