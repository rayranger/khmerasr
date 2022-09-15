from crypt import methods
from dataclasses import dataclass
from src import app
from flask import render_template, redirect, url_for
from src.forms.register_form import RegisterForm
from src.forms.sing_in_form import SigninForm
from src.forms.speaker_register_form import SpeakerRegisterForm
from src.forms.record_form import StartRecordForm, SubmitRecordForm
from src.controllers import user_controller, auth_controller, speaker_controller
from flask_login import login_required, current_user

userController = user_controller.UserController()
authController = auth_controller.AuthController()
speakerController = speaker_controller.SpeakerController()

@app.route('/sign-in', methods=['GET', 'POST'])
def signin_page():
    sign_in_form = SigninForm()
    if authController.sign_in(sign_in_form=sign_in_form):
        return redirect(url_for('home_page'))
    return render_template('sign-in.html', sign_in_form = sign_in_form)

@app.route('/sign-out')
def signout_page():
    authController.sign_out()
    return redirect(url_for('signin_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if authController.register(register_form=register_form):
        return redirect(url_for('home_page'))
    return render_template('register.html', register_form=register_form)

@app.route('/speaker-register', methods=['GET', 'POST'])
def speaker_register_page():
    speaker_register_form = SpeakerRegisterForm()
    if speaker_register_form.validate_on_submit():
        if speakerController.create_speaker(
                first_name=speaker_register_form.first_name.data,
                last_name=speaker_register_form.last_name.data,
                gender=speaker_register_form.gender.data,
                age=speaker_register_form.age.data,
                occupation=speaker_register_form.occupation.data,
                phone_number=speaker_register_form.phone_number.data,
                user_id=current_user.id
            ):
            return redirect(url_for('record_page'))
    return render_template('speaker_register.html', speaker_register_from=speaker_register_form)

@app.route("/google-signin")
def google_signin():
    authorizationUrl = authController.google_sign_in()
    return redirect(authorizationUrl)

@app.route("/callback")
def callback():
    authController.google_callback()
    return redirect(url_for('record_page'))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/record', methods=['GET', 'POST'])
@login_required
def record_page():
    start_record_form = StartRecordForm()
    save_record_form = SubmitRecordForm()
    return render_template('record.html', start_record_form=start_record_form, save_record_form=save_record_form)
