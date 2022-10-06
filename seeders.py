import email
from unicodedata import name
from src import db
from src.models import audio, recording, role, speaker, user, record_config, task
from datetime import date, datetime

# create role
role_1 = role.Role(
    name='admin', 
)
role_2 = role.Role(
    name='user', 
)
db.session.add_all([role_1, role_2])
db.session.commit()

# create user
user_1 = user.User(
    username='raychannudam',
    email='raychannudam@gmail.com',
    password='raychannudam',
)
user_2 = user.User(
    username='yichandara',
    email='yichandara@gmail.com',
    password='yichandara',
)
db.session.add_all([user_1, user_2])

# create user_role
user_1.roles.append(role_1)
user_1.roles.append(role_2)
user_2.roles.append(role_2)
db.session.commit()

#create speaker
speaker_1 = speaker.Speaker(
    first_name = "Chandara",
    last_name='Yi',
    gender="Male",
    age=20,
    occupation='Student',
    phone_number='017701656',
    user_id=2,
)
db.session.add(speaker_1)
db.session.commit()

#create recode_config
record_config_1 = record_config.RecordConfig(
    channel = 1,
    sample_rate = 16000,
    number_of_sample = 1024,
    duration = 3,
)
record_config_2 = record_config.RecordConfig(
    channel = 1,
    sample_rate = 16000,
    number_of_sample = 3200,
    duration = 3,
)
db.session.add_all([record_config_1, record_config_2])
db.session.commit()

#create task
task_1 = task.Task(
    name="Task A",
    description="Description for task A",
    record_config_id=1,
    created_user_id=1
)
task_2 = task.Task(
    name="Task B",
    description="Description for task B",
    record_config_id=1,
    created_user_id=1
)
task_3 = task.Task(
    name="Task C",
    description="Description for task C",
    record_config_id=2,
    created_user_id=1
)
task_4 = task.Task(
    name="Task D",
    description="Description for task D",
    record_config_id=2,
    created_user_id=1
)
db.session.add_all([task_1, task_2, task_3, task_4])
db.session.commit()

# create recording
recording_1 = recording.Recording(
    transcript = "This is recording transcript for recording_1",
    instruction = "This is instruction for recording_1",
    sample_filename = "file_1.wav",
    task_id = 1
)
recording_11 = recording.Recording(
    transcript = "This is recording transcript for recording_1.1",
    instruction = "This is instruction for recording_1.1",
    sample_filename = "file_11.wav",
    task_id = 1
)
recording_12 = recording.Recording(
    transcript = "This is recording transcript for recording_1.2",
    instruction = "This is instruction for recording_1.2",
    sample_filename = "file_12.wav",
    task_id = 1
)
recording_13 = recording.Recording(
    transcript = "This is recording transcript for recording_1.3",
    instruction = "This is instruction for recording_1.3",
    sample_filename = "file_13.wav",
    task_id = 1
)
recording_14 = recording.Recording(
    transcript = "This is recording transcript for recording_1.4",
    instruction = "This is instruction for recording_1.4",
    sample_filename = "file_14.wav",
    task_id = 1
)
recording_15 = recording.Recording(
    transcript = "This is recording transcript for recording_1.5",
    instruction = "This is instruction for recording_1.5",
    sample_filename = "file_15.wav",
    task_id = 1
)
recording_2 = recording.Recording(
    transcript = "This is recording transcript for recording_2",
    instruction = "This is instruction for recording_2",
    sample_filename = "file_2.wav",
    task_id = 2
)
recording_3 = recording.Recording(
    transcript = "This is recording transcript for recording_3",
    instruction = "This is instruction for recording_3",
    sample_filename = "file_3.wav",
    task_id = 3
)
recording_4 = recording.Recording(
    transcript = "This is recording transcript for recording_4",
    instruction = "This is instruction for recording_4",
    sample_filename = "file_4.wav",
    task_id = 4
)
db.session.add_all([recording_1, recording_11, recording_12, recording_13, recording_14, recording_15, recording_2, recording_3, recording_4])
db.session.commit()