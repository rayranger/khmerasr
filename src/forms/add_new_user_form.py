from flask_wtf import FlaskForm
from wtforms import SubmitField

class AddNewUserForm(FlaskForm):
    submit = SubmitField(label='Add new user')