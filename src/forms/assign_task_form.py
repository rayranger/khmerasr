from flask_wtf import FlaskForm
from wtforms import SubmitField

class AssignTaskForm(FlaskForm):
    submit = SubmitField(label="Create new task")