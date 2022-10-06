from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

class RecordingForm(FlaskForm):
    sample_file = FileField(label="Sample audio file", validators=[DataRequired()])
    submit = SubmitField(label="Save new recording")

