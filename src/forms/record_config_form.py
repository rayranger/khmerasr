from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

class RecordConfigForm(FlaskForm):
    submit = SubmitField(label="Save Change")