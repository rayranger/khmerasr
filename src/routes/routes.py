from src import app
from flask import render_template, redirect, url_for, jsonify, request
from src.forms.register_form import RegisterForm
from src.forms.sing_in_form import SigninForm
from src.forms.record_config_form import RecordConfigForm
from src.forms.speaker_register_form import SpeakerRegisterForm
from src.forms.record_form import StartRecordForm, SubmitRecordForm
from src.controllers import user_controller, auth_controller, speaker_controller, record_controller, record_config_controller
from flask_login import login_required, current_user

userController = user_controller.UserController()
authController = auth_controller.AuthController()
speakerController = speaker_controller.SpeakerController()
recordController = record_controller.RecordController()
recordConfigController = record_config_controller.RecordConfigController()

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
    if authController.google_callback():
        return redirect(url_for('record_page'))
    else:
        return redirect(url_for('speaker_register_page'))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/record', methods=['GET', 'POST'])
@login_required
def record_page():
    start_record_form = StartRecordForm()
    save_record_form = SubmitRecordForm()
    return render_template('record.html', start_record_form=start_record_form, save_record_form=save_record_form)

@app.route('/record_audio', methods=['POST'])
def record_audio_page():
    recordName = recordController.record(username=current_user.username)
    recordController.create_record(
            filename=recordName,
            speaker_id=current_user.speaker.id,
            category_id=1
        )

    return jsonify(recordName)

@app.route('/dashboard')
@login_required
def dashboard_page():
    roles = current_user.roles
    flag = 0
    for role in roles:
        if role.name == 'admin':
            return render_template('dashboard/dashboard.html', current_user=current_user)
    return ('Permission Denied')

# dashboard-user

@app.route('/dashboard/users')
def dashboard_user_page():
    users = userController.get_all_user()
    return render_template('dashboard/registered_user.html', users=users)

@app.route('/dashboard/user/delete/<int:id>', methods=['GET', 'DELETE'])
def dashboard_delete_user(id):
    userController.delete_user(id=id)
    return redirect(url_for('dashboard_user_page'))

# dashboard-speaker

@app.route('/dashboard/speakers')
def dashboard_speaker_page():
    speakers = speakerController.get_all_speaker()
    return render_template('dashboard/registered_speaker.html', speakers = speakers)

@app.route('/dashboard/speaker/delete/<int:id>')
def dashboard_delete_speaker(id):
    speakerController.delete_speaker(id=id)
    return redirect(url_for('dashboard_speaker_page'))

# dashboard-record_configuration

@app.route('/dashboard/record-configuration', methods=['GET', 'POST'])
def dashboard_record_configuration_page():
    recordConfigs = recordConfigController.get_all_record_config()
    for recordConfig in recordConfigs:
        config = recordConfig
    record_config_form = RecordConfigForm()
    if request.form.get("channel") == 'mono':
        channelValue = 1
    else:
        channelValue = 2
    if request.form:
        updatedUser = recordConfigController.update_record_config(
            id=config.id,
            duration=request.form.get("duration"),
            frame_per_buffer=request.form.get("frame_per_buffer"),
            channel=channelValue,
            sample_rate=request.form.get("framerate"),
            bit_rate=request.form.get("framerate")
        )
    return render_template('dashboard/record_configuration.html', record_config_form=record_config_form, recordConfig=config)

# dashboard-recorded_audio

@app.route('/dashboard/record-audio')
def dashboard_record_audio():
    records = recordController.get_all_record()
    print(records)
    return render_template('dashboard/record_audio.html', records = records)
