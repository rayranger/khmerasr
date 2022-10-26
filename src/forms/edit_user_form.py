from flask_wtf import FlaskForm
from wtforms import SubmitField

class EditUserForm(FlaskForm):
    submit = SubmitField(label='Update')