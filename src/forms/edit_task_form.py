from flask_wtf import FlaskForm
from wtforms import SubmitField

class EditTaskForm(FlaskForm):
    submit = SubmitField(label='Edit task')