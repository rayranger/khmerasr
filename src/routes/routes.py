
from datetime import datetime
from src import app
from flask import render_template, redirect, url_for, jsonify, request
from werkzeug.utils import secure_filename
from src.forms.recording_form import RecordingForm
from src.forms.register_form import RegisterForm
from src.forms.sing_in_form import SigninForm
from src.forms.record_config_form import RecordConfigForm
from src.forms.speaker_register_form import SpeakerRegisterForm
from src.forms.record_form import StartRecordForm, SubmitRecordForm
from src.forms.assign_task_form import AssignTaskForm
from src.controllers import audio_controller, user_controller, auth_controller, speaker_controller, record_config_controller, task_controller, recording_controller
from flask_login import login_required, current_user

userController = user_controller.UserController()
authController = auth_controller.AuthController()
speakerController = speaker_controller.SpeakerController()
audioController = audio_controller.AudioController()
recordConfigController = record_config_controller.RecordConfigController()
taskController = task_controller.TaskController()
recordingController = recording_controller.RecordingController()

@app.route('/sign-in', methods=['GET', 'POST'])
def signin_page():
    sign_in_form = SigninForm()
    attemped_user = authController.sign_in(sign_in_form=sign_in_form)
    if attemped_user:
        for user_role in attemped_user.roles:
            if user_role.name == 'admin': 
                return render_template('dashboard/overview.html')
        return redirect(url_for('task_page'))
    return render_template('sign-in.html', sign_in_form = sign_in_form)

@app.route('/sign-out')
def signout_page():
    authController.sign_out()
    return redirect(url_for('home_page'))

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
        return redirect(url_for('task_page'))
    else:
        return redirect(url_for('speaker_register_page'))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/task')
@login_required
def task_page():
    if current_user.speaker:
        speaker_id = current_user.speaker.id
        tasks = taskController.get_all_task()
        total_recordings = []
        total_remaining_recordings = []
        for task in tasks:
            remaining_recordings = recordingController.getRemainingRecording(
                speaker_id=speaker_id,
                selected_task=task
            )
            total_remaining_recordings.append(len(remaining_recordings))
            total_recordings.append(len(task.recordings))
        return render_template('task.html', tasks=tasks, total_recordings=total_recordings, total_remaining_recordings=total_remaining_recordings)
    return redirect(url_for('speaker_register_page'))

@app.route('/task-detail/<int:id>')
@login_required
def task_detail_page(id):
    speaker_id = current_user.speaker.id
    selected_task = taskController.is_existed(data=id)
    filename = f'{current_user.username}_{str(datetime.now().strftime("%d%m%Y_%H%M%S"))}.ogg'
    recording_config = recordConfigController.is_existed(data=selected_task.record_config_id)
    remaining_recordings = recordingController.getRemainingRecording(
        speaker_id=speaker_id,
        selected_task=selected_task
    )
    audioController.getRecordConfig(
        frame_per_buffer=recording_config.number_of_sample,
        channel=recording_config.channel,
        rate=recording_config.sample_rate,
        filetype=recording_config.filetype,
        duration=recording_config.duration
    )
    if len(remaining_recordings) > 0:
        return render_template('task_detail.html', selected_task=selected_task, recording=remaining_recordings[0], recording_config=recording_config, filename=filename)
    else:
        return render_template('completed.html')

@app.route('/save-audio', methods=['POST'])
def save_audio():
    files = request.files
    file_to_save = files.get('audioFile')
    file_to_save.save(f"src/static/storage/audios/recordings/{file_to_save.filename}")
    return jsonify(file_to_save.filename)


@app.route('/recording', methods=['GET'])
def record_page():
    id = request.args.get('id')
    filename = request.args.get('filename')
    speaker_id = current_user.speaker.id
    selected_task = taskController.is_existed(data=id)
    remaining_recordings = recordingController.getRemainingRecording(
        speaker_id=speaker_id,
        selected_task=selected_task
    )
    print(len(remaining_recordings))
    new_audio = audioController.create_audio(
        filename=filename,
        recording_id=remaining_recordings[0].id,
        speaker_id=speaker_id
    )
    if len(remaining_recordings) > 0:
        if len(remaining_recordings) == 1:
            return jsonify(render_template('task_detail_model.html', recording=remaining_recordings[0], selected_task=selected_task))
        return jsonify(render_template('task_detail_model.html', recording=remaining_recordings[1], selected_task=selected_task))

    else: 
        return jsonify('Done')
