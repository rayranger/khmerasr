from curses import flash
from datetime import datetime
import flask
from src import app
from flask import render_template, redirect, url_for, jsonify, request, flash
from werkzeug.utils import secure_filename
from src.forms.edit_speaker_form import EditSpeakerForm
from src.forms.recording_form import RecordingForm
from src.forms.register_form import RegisterForm
from src.forms.sing_in_form import SigninForm
from src.forms.record_config_form import RecordConfigForm
from src.forms.speaker_register_form import SpeakerRegisterForm
from src.forms.add_new_user_form import AddNewUserForm
from src.forms.edit_user_form import EditUserForm
from src.forms.assign_task_form import AssignTaskForm
from src.models import user, speaker
from src.controllers import audio_controller, user_controller, auth_controller, speaker_controller, record_config_controller, task_controller, recording_controller, role_controller
from flask_login import login_required, current_user
import functools

userController = user_controller.UserController()
authController = auth_controller.AuthController()
speakerController = speaker_controller.SpeakerController()
audioController = audio_controller.AudioController()
recordConfigController = record_config_controller.RecordConfigController()
taskController = task_controller.TaskController()
recordingController = recording_controller.RecordingController()
roleController = role_controller.RoleController()

def admin_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        for user_role in current_user.roles:
            if user_role.name == "admin":
                return f(*args, **kwargs)
            else:
                flash("You need to be an admin to view this page.")
                return redirect(url_for('home_page'))
    return wrap

# dashboard part

@app.route('/dashboard')
@login_required
@admin_required
def dashboard_page():

    return render_template('dashboard/dashboard.html', current_user=current_user)

#dashboard-overview
@app.route('/dashboard/overview')
@login_required
def dashboard_overview_page():
    return render_template('dashboard/overview.html')

# dashboard-user

@app.route('/dashboard/users', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard_user_page():
    add_new_user_form = AddNewUserForm()
    edit_user_form = EditUserForm()
    users = userController.get_all_user()
    roles = roleController.get_all_roles()
    is_active = True
    edit_is_active = True
    if flask.request.method == 'POST':
        if request.form.get('username') and add_new_user_form.validate_on_submit():
            if request.form.get('is_active') != 'on':
                is_active = False
            role = roleController.is_existed(id=int(request.form.get('role')))
            new_user = userController.create_user(
                username=request.form.get('username'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                role=role
            )
        if request.form.get('edit_username'):
            if request.form.get('edit_is_active') != 'on':
                edit_is_active = False
            update_user = user.User(
                username = request.form.get('edit_username'),
                email = request.form.get('edit_email'),
                is_active = edit_is_active
            )
            userController.update_user(
                new_user_obj=update_user,
                id=int(request.form.get('edit_id'))
            )
        print(request.form.getlist('edit_roles'))
            
    return render_template('dashboard/registered_user.html', users=users, add_new_user_form=add_new_user_form, roles=roles, edit_user_form=edit_user_form)

@app.route('/dashboard/user/delete/<int:id>', methods=['GET', 'DELETE'])
@login_required
@admin_required
def dashboard_delete_user(id):
    userController.delete_user(id=id)
    return redirect(url_for('dashboard_user_page'))

# dashboard-speaker
@app.route('/dashboard/speakers', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard_speaker_page():
    speakers = speakerController.get_all_speaker()
    add_new_speaker_form = SpeakerRegisterForm()
    edit_speaker_form = EditSpeakerForm()
    users = userController.get_all_user()
    if flask.request.method == 'POST':
        if request.form.get('user_id'):
            user_to_create = userController.is_existed(data=int(request.form.get('user_id')))
            if user_to_create.speaker:
                flash('This user had already registerd as a speaker')
            else:
                if add_new_speaker_form.submit():
                    new_speaker = speakerController.create_speaker(
                        first_name=request.form.get('firstname'),
                        last_name=request.form.get('lastname'),
                        gender=request.form.get('gender'),
                        age=int(request.form.get('age')),
                        occupation=request.form.get('occupation'),
                        phone_number=request.form.get('phone_number'),
                        user_id=int(request.form.get('user_id'))
                    )
            return redirect(url_for('dashboard_speaker_page'))
        if edit_speaker_form.submit():
            update_speaker = speaker.Speaker(
                first_name = request.form.get('edit_firstname'),
                last_name = request.form.get('edit_lastname'),
                gender = request.form.get('edit_gender'),
                age = int(request.form.get('edit_age')),
                occupation = request.form.get('edit_occupation'),
                phone_number = request.form.get('edit_phone_number')
            )
            speakerController.update_speaker(
                new_speaker_obj=update_speaker,
                id=int(request.form.get('edit_id'))
            )
            return redirect(url_for('dashboard_speaker_page'))
    return render_template('dashboard/registered_speaker.html', speakers = speakers, add_new_speaker_form=add_new_speaker_form, users=users, edit_speaker_form=edit_speaker_form)

@app.route('/dashboard/speaker/delete/<int:id>')
@login_required
@admin_required
def dashboard_delete_speaker(id):
    speakerController.delete_speaker(id=id)
    return redirect(url_for('dashboard_speaker_page'))

# dashboard-record_configuration

@app.route('/dashboard/record-configuration', methods=['GET', 'POST'])
@login_required
@admin_required
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
@login_required
@admin_required
def dashboard_delete_record_config(id):
    recordConfig = recordConfigController.is_existed(data=id)
    if recordConfig:
        recordConfigController.delete_record_config(id=id)
    return redirect(url_for('dashboard_record_configuration_page'))

# dashboard-audio

@app.route('/dashboard/record-audio')
@login_required
@admin_required
def dashboard_record_audio():
    audios = audioController.get_all_audio()
    print(audios)
    return render_template('dashboard/record_audio.html', audios = audios)

@app.route('/dashboard/record-audio/delete/<int:id>')
@login_required
@admin_required
def dashboard_delete_record_audio(id):
    if audioController.is_existed(data=id):   
        audioController.delete_audio(id=id)
    return redirect(url_for('dashboard_record_audio'))

# dashboard-assign_task

@app.route('/dashboard/assign-task', methods=['GET', 'POST'])
@login_required
@admin_required
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
@login_required
@admin_required
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
@login_required
@admin_required
def dashboard_delete_assign_task(id):
    assign_task = taskController.is_existed(data=id)
    if assign_task:
        taskController.delete_taskr(id=id)
        return redirect(url_for('dashboard_assign_task'))
    else:
        return None

@app.route('/dashboard/recording/delete/<int:id>/<int:task_id>')
@login_required
@admin_required
def dashboard_delete_recording(id, task_id):
    recording = recordingController.is_existed(data=id)
    if recording:
        recordingController.delete_task_record(id)
        return redirect(url_for('dashboard_assign_task_detail', id=task_id))
    else:
        return None


