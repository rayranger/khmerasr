from flask_wtf import FlaskForm
from wtforms import SubmitField

class ExportDataForm (FlaskForm):
    submit = SubmitField(label='Export')