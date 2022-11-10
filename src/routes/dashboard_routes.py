import flask
from src import app
from flask import render_template, redirect, url_for, request, flash, send_file
from src.forms.edit_speaker_form import EditSpeakerForm
from src.forms.recording_form import RecordingForm
from src.forms.record_config_form import RecordConfigForm
from src.forms.edit_recording_form import EditRecordingForm
from src.forms.speaker_register_form import SpeakerRegisterForm
from src.forms.add_new_user_form import AddNewUserForm
from src.forms.edit_user_form import EditUserForm
from src.forms.assign_task_form import AssignTaskForm
from src.forms.edit_task_form import EditTaskForm
from src.forms.export_data_form import ExportDataForm
from src.models import user, speaker, task, recording
from src.controllers import audio_controller, user_controller, auth_controller, speaker_controller, record_config_controller, task_controller, recording_controller, role_controller, export_data_controller, export_history_controller
from flask_login import login_required, current_user
import functools
import os
import shutil

userController = user_controller.UserController()
authController = auth_controller.AuthController()
speakerController = speaker_controller.SpeakerController()
audioController = audio_controller.AudioController()
recordConfigController = record_config_controller.RecordConfigController()
taskController = task_controller.TaskController()
recordingController = recording_controller.RecordingController()
roleController = role_controller.RoleController()
exportDataController = export_data_controller.ExportDataController()
exportHistoryController = export_history_controller.ExportHistoryController()

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


@app.route('/dashboard')
@login_required
@admin_required
def dashboard_page():
    return redirect(url_for('dashboard_overview_page'))
    # return render_template('dashboard/dashboard.html', current_user=current_user)

#dashboard-overview
@app.route('/dashboard/overview')
@login_required
def dashboard_overview_page():
    total_speaker = len(speakerController.get_all_speaker())
    total_recording = 0
    tasks = taskController.get_all_task()
    for taskItem in tasks:
        total_recording = total_recording + len(taskItem.recordings)
    total_audio = len(audioController.get_all_audio())

    return render_template('dashboard/overview.html', total_speaker=total_speaker, total_recording=total_recording, total_audio=total_audio)

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
            return redirect(url_for('dashboard_user_page'))
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
            return redirect(url_for('dashboard_user_page'))
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
            user_to_create = userController.findUserById(data=int(request.form.get('user_id')))
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
    if audioController.findAudioById(data=id):   
        audioController.delete_audio(id=id)
    return redirect(url_for('dashboard_record_audio'))

# dashboard-assign_task
@app.route('/dashboard/assign-task', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard_assign_task():
    assign_task_form = AssignTaskForm()
    edit_task_form = EditTaskForm()
    recordConfigs = recordConfigController.get_all_record_config()
    tasks = taskController.get_all_task()
    if request.form.get('task_name'):
        taskController.create_task(
            name=request.form.get('task_name'),
            description=request.form.get('task_description'),
            created_user_id=current_user.id,
            record_config_id=request.form.get('record_config')
        )
        return redirect(url_for('dashboard_assign_task'))
    if edit_task_form.validate_on_submit():
        update_id = request.form.get('edit_task_id')
        update_task = task.Task(
            name = request.form.get('edit_task_name'),
            description = request.form.get('edit_task_description'),
            record_config_id = request.form.get('edit_record_config'),
            created_user_id = current_user.id
        )
        taskController.update_task(
            new_task_obj=update_task,
            id=update_id
        )
    return render_template('dashboard/assign_task.html', tasks=tasks, assign_task_form=assign_task_form, recordConfigs=recordConfigs, edit_task_form=edit_task_form)

@app.route('/dashboard/assign-task/detail/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard_assign_task_detail(id):
    recording_form = RecordingForm()
    edit_recording_form = EditRecordingForm()
    seleted_task = taskController.findTaskById(data=id)
    if recording_form.validate_on_submit():
        file = recording_form.sample_file.data
        file.save(f"src/static/storage/audios/samples/{file.filename}")
        recordingController.create_task_record(
            transcript=request.form.get("transcript"),
            instruction=request.form.get("instruction"),
            sample_filename=file.filename,
            task_id=seleted_task.id
        )
    if edit_recording_form.validate_on_submit():
        id = int(request.form.get('edit_id'))
        recordingItem = recordingController.is_existed(data=id)
        file = edit_recording_form.edit_sample_file.data
        if file:
            file.save(f"src/static/storage/audios/samples/{file.filename}")
            filename = file.filename
            os.remove(f"src/static/storage/audios/samples/{recordingItem.sample_filename}")
        else:
            filename = recordingItem.sample_filename

        update_recording = recording.Recording(
            transcript = request.form.get('edit_transcript'),
            instruction = request.form.get('edit_instruction'),
            sample_filename = filename,
        )
        recordingController.update_task_record(
            new_task_record=update_recording,
            id=id
        )

       
    return render_template('dashboard/assign_task_detail.html',
    seleted_task=seleted_task, recording_form=recording_form, edit_recording_form=edit_recording_form)

@app.route('/dashboard/assign-task/delete/<int:id>')
@login_required
@admin_required
def dashboard_delete_assign_task(id):
    assign_task = taskController.findTaskById(data=id)
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

# dashboard-export-data
@app.route('/dashboard/export-data', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard_export_data():
    export_data_form = ExportDataForm()
    recordConfigs = recordConfigController.get_all_record_config()
    tasks = taskController.get_all_task()
    export_histories = exportHistoryController.get_all_export_history()
    audioList = []
    audioList_final = []
    audioList_final_name = []
    speaker_info_list = []
    speaker_info_list_csv =[]
    if export_data_form.validate_on_submit():
        audios = audioController.getAllAudioByTask(taskId=int(request.form.get('export_task_id')))
        if request.form.get('export_record_config_id') != 'All record config':
            for audioItem in audios:
                audio_config = audioItem.recording.task.record_config_id
                if audio_config == int(request.form.get('export_record_config_id')):
                    audioList.append(audioItem)
        else:
            audioList = audios

        if request.form.get('export_gender') != 'All Genders':
            if request.form.get('export_gender') == 'Male':
                for audioItem in audioList:
                    if audioItem.speaker.gender == 'Male':
                        audioList_final.append(audioItem)
            else:
                for audioItem in audioList:
                    if audioItem.speaker.gender == 'Female':
                        audioList_final.append(audioItem)
        else:
            audioList_final = audioList
        
        for audioItem_ in audioList_final:
            audioList_final_name.append(audioItem_.filename)


        for audioItem in audioList_final:
            if len(speaker_info_list) > 0:
                for speaker_info in speaker_info_list:
                    if audioItem.speaker.id == speaker_info.id:
                        break
                    speaker_info_list.append(audioItem.speaker)
            else:
                speaker_info_list.append(audioItem.speaker)

        for speakerItem in speaker_info_list:
            speaker_info_csv = []
            speaker_info_csv.append(speakerItem.first_name)
            speaker_info_csv.append(speakerItem.last_name)
            speaker_info_csv.append(speakerItem.gender)
            speaker_info_csv.append(speakerItem.age)
            speaker_info_csv.append(speakerItem.occupation)
            speaker_info_csv.append(speakerItem.phone_number)
            speaker_info_list_csv.append(speaker_info_csv)
           
        direcntory_name = exportDataController.create_csv_file(
            directory_name= request.form.get('export_name'),
            filename='speaker_info',
            fieldList= ['Firstname', 'Lastname', 'Gender', 'Age', 'Occupation', 'Phone number'],
            itemList= speaker_info_list_csv,
        )

        zip_name = exportDataController.create_zip_file(
            zipname = f'{direcntory_name}.zip',
            directory_name = direcntory_name,
            csv_filename = 'speaker_info.csv',
            filenames=audioList_final_name
        )

        file_to_send_path = f'static/exported/{direcntory_name}/{zip_name}'

        @flask.after_this_request
        def delete_file(res):
            task = taskController.findTaskById(data=int(request.form.get('export_task_id')))
            exportHistoryController.create_export_history(
                task_name=task.name,
                record_config_id=request.form.get('export_record_config_id'),
                gender=request.form.get('export_gender'),
                export_name=request.form.get('export_name'),
                user_id=current_user.id
            )
            shutil.rmtree(f'src/static/exported/{direcntory_name}')
            return res

        return send_file(file_to_send_path, as_attachment=True)

    return render_template('dashboard/export_data.html', export_data_form=export_data_form, tasks=tasks, recordConfigs=recordConfigs, export_histories=export_histories)

@app.route('/dashboard/export-data/delete/<int:id>')
def dashboard_delete_export_data(id):
    req = exportHistoryController.delete_export_history(id=id)
    if req:
        return redirect(url_for('dashboard_export_data'))
    else:
        flash('History you attemped to delete is not exist.', 'danger')

