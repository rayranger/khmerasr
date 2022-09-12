from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    # user
    username = StringField(label='Username: ', validators=[Length(min=4, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])

    #speaker
    first_name = StringField(label='Firstname: ', validators=[DataRequired()])
    last_name = StringField(label='Lastname: ', validators=[DataRequired()])
    gender = StringField(label='Gender: ', validators=[DataRequired()])
    age = StringField(label='Age: ', validators=[DataRequired()])
    occupation = StringField(label='Occupation', validators=[DataRequired()])
    phone_number = StringField(label='Phone number', validators=[DataRequired()])

    #submit
    submit = SubmitField(label='Create an Account', validators=[])



