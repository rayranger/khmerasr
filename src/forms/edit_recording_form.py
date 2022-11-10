from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField

class EditRecordingForm(FlaskForm):
    edit_sample_file = FileField(label="Edit sample audio file")
    submit = SubmitField(label="Save new recording")

