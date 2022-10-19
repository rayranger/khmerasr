
from datetime import datetime
import os
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
        return redirect(url_for('task_page'))
    else:
        return redirect(url_for('speaker_register_page'))

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/task')
@login_required
def task_page():
    tasks = taskController.get_all_task()
    return render_template('task.html', tasks=tasks)

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
    return render_template('task_detail.html', selected_task=selected_task, recording=remaining_recordings[0], recording_config=recording_config, filename=filename)

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
    new_audio = audioController.create_audio(
        filename=filename,
        recording_id=remaining_recordings[0].id,
        speaker_id=speaker_id
    )
    return jsonify(render_template('task_detail_model.html', recording=remaining_recordings[1], selected_task=selected_task))






# dashboard part

@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard/dashboard.html', current_user=current_user)

#dashboard-overview
@app.route('/dashboard/overview')
@login_required
def dashboard_overvie_page():
    return render_template('dashboard/overview.html')

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
    record_config_form = RecordConfigForm()
    if request.form.get('channel') == '1':
        channel = 1
    else:
        channel = 2
    if request.form:
        recordConfigController.create_record_config(
            duration=request.form.get('duration'),
            number_of_sample=request.form.get('number_of_sample_input'),
            channel=channel,
            sample_rate=request.form.get('sample_rate_input'),
            filetype=request.form.get('filetype')
        ) 
        return redirect(url_for('dashboard_record_configuration_page'))
    return render_template('dashboard/record_configuration.html', recordConfigs=recordConfigs, record_config_form=record_config_form)

@app.route('/dashboard/record-configuration/delete/<int:id>', methods=['GET','DELETE'])
def dashboard_delete_record_config(id):
    recordConfig = recordConfigController.is_existed(data=id)
    if recordConfig:
        recordConfigController.delete_record_config(id=id)
    return redirect(url_for('dashboard_record_configuration_page'))

# dashboard-audio

@app.route('/dashboard/record-audio')
def dashboard_record_audio():
    audios = audioController.get_all_audio()
    print(audios)
    return render_template('dashboard/record_audio.html', audios = audios)

@app.route('/dashboard/record-audio/delete/<int:id>')
def dashboard_delete_record_audio(id):
    if audioController.is_existed(data=id):   
        audioController.delete_audio(id=id)
    return redirect(url_for('dashboard_record_audio'))

# dashboard-assign_task

@app.route('/dashboard/assign-task', methods=['GET', 'POST'])
def dashboard_assign_task():
    assign_task_form = AssignTaskForm()
    recordConfigs = recordConfigController.get_all_record_config()
    tasks = taskController.get_all_task()
    if request.form.get('sample_file'):
        print('Added new recording')
    if request.form.get('task_name'):
        taskController.create_task(
            name=request.form.get('task_name'),
            description=request.form.get('task_description'),
            created_user_id=current_user.id,
            record_config_id=request.form.get('record_config')
        )
        return redirect(url_for('dashboard_assign_task'))
    return render_template('dashboard/assign_task.html', tasks=tasks, assign_task_form=assign_task_form, recordConfigs=recordConfigs)

@app.route('/dashboard/assign-task/detail/<int:id>', methods=['GET', 'POST'])
def dashboard_assign_task_detail(id):
    recording_form = RecordingForm()
    seleted_task = taskController.is_existed(data=id)
    if recording_form.validate_on_submit():
        file = recording_form.sample_file.data
        file.save(f"src/static/storage/audios/samples/{file.filename}")
        recordingController.create_task_record(
            transcript=request.form.get("transcript"),
            instruction=request.form.get("instruction"),
            sample_filename=file.filename,
            task_id=seleted_task.id
        )
    return render_template('dashboard/assign_task_detail.html', seleted_task=seleted_task, recording_form=recording_form)

@app.route('/dashboard/assign-task/delete/<int:id>')
def dashboard_delete_assign_task(id):
    assign_task = taskController.is_existed(data=id)
    if assign_task:
        taskController.delete_taskr(id=id)
        return redirect(url_for('dashboard_assign_task'))
    else:
        return None

@app.route('/dashboard/recording/delete/<int:id>/<int:task_id>')
def dashboard_delete_recording(id, task_id):
    recording = recordingController.is_existed(data=id)
    if recording:
        recordingController.delete_task_record(id)
        return redirect(url_for('dashboard_assign_task_detail', id=task_id))
    else:
        return None


