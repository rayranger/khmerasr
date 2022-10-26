from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SpeakerRegisterForm(FlaskForm):
    first_name = StringField(label='Firstname: ', validators=[DataRequired()])
    last_name = StringField(label='Lastname: ', validators=[DataRequired()])
    gender = StringField(label='Gender: ', validators=[DataRequired()])
    age = StringField(label='Age: ', validators=[DataRequired()])
    occupation = StringField(label='Occupation', validators=[DataRequired()])
    phone_number = StringField(label='Phone number', validators=[DataRequired()])
    submit = SubmitField(label="Add new speaker", validators=[DataRequired()])