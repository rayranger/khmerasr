from flask_wtf import FlaskForm
from wtforms import SubmitField

class StartRecordForm(FlaskForm):
    submit = SubmitField(label="Start record")

class SubmitRecordForm(FlaskForm):
    submit = SubmitField(label="Submit record")