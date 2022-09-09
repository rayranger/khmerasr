from unicodedata import name
from src import db
from src.models import record, record_category, role, speaker, user, record_config, task
from datetime import date, datetime

now = datetime.now()
TODAY_DATE_TIME = now.strftime("%d/%m/%Y %H:%M:%S")

# create user
user_1 = user.User(username='raychannudam', email='raychannudam@gmail.com', password='raychannudam', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
user_2 = user.User(username='yichandara', email='yichandara@gmail.com', password='yichandara', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
user_3 = user.User(username='vuthypanha', email='vuthypanha@gmail.com', password='vuthypanha', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
user_4 = user.User(username='thornmanivourn', email='thornmanivourn@gmail.com', password='thornmanivourn', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([user_1,user_2,user_3,user_4])
db.session.commit()

# create role
role_1 = role.Role(name='admin', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
role_2 = role.Role(name='user', created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([role_1, role_2])
db.session.commit()

# create relationship between role and user
user_1.roles.append(role_1)
user_1.roles.append(role_2)
user_2.roles.append(role_1)
user_2.roles.append(role_2)
user_3.roles.append(role_2)
user_3.roles.append(role_2)
db.session.commit()

# create record category
record_category_1 = record_category.RecordCategory(name="Category A", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_2 = record_category.RecordCategory(name="Category B", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_3 = record_category.RecordCategory(name="Category C", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_4 = record_category.RecordCategory(name="Category D", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([record_category_1, record_category_2, record_category_3, record_category_4])
db.session.commit()

# create speaker
speaker_1 = speaker.Speaker(first_name='Chann Udam', last_name='Ray', gender='M', age=20, occupation='Student', phone_number='017701656', user_id=1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
speaker_2 = speaker.Speaker(first_name='Chandara', last_name='Yi', gender='M', age=21, occupation='Student', phone_number='012910362', user_id=2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
speaker_3 = speaker.Speaker(first_name='Panha', last_name='Vuthy', gender='M', age=19, occupation='Student', phone_number='017586670', user_id=3, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
speaker_4 = speaker.Speaker(first_name='Manivourn', last_name='Thorn', gender='M', age=21, occupation='Student', phone_number='099814655', user_id=4, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([speaker_1, speaker_2, speaker_3, speaker_4])
db.session.commit()

# create record category
record_category_1 = record_category.RecordCategory(name="Category A", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_2 = record_category.RecordCategory(name="Category B", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_3 = record_category.RecordCategory(name="Category C", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_category_4 = record_category.RecordCategory(name="Category D", created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

# create record 
record_1 = record.Record(filename='file1.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=1, speaker_id = 1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_2 = record.Record(filename='file2.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=2, speaker_id = 1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_3 = record.Record(filename='file3.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=1, speaker_id = 2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_4 = record.Record(filename='file4.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=2, speaker_id = 2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_5 = record.Record(filename='file5.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=1, speaker_id = 3, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_6 = record.Record(filename='file6.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=2, speaker_id = 3, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_7 = record.Record(filename='file7.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=1, speaker_id = 4, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_8 = record.Record(filename='file8.wav', filesize='1000', filetype='wav', channel=1, sample_framerate=1000, sample_frame=1000, total_frame=10000, duration=5, category_id=2, speaker_id = 4, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([record_1, record_2, record_3, record_4, record_5, record_6, record_7, record_8])
db.session.commit()

# create record config
record_config_1 = record_config.RecordConfig(duration=5, frame_per_buffer=1000, channel=1, rate=1000, user_id=1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
record_config_2 = record_config.RecordConfig(duration=5, frame_per_buffer=1600, channel=1, rate=800, user_id=2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([record_config_1, record_config_2])
db.session.commit()

# create task
task_1 = task.Task(name='Task A', description='This is desc from Task A', instruction='This is inst from Task A', sample_audio_name='file1.wav', created_user_id = 1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
task_2 = task.Task(name='Task B', description='This is desc from Task B', instruction='This is inst from Task B', sample_audio_name='file2.wav', created_user_id = 1, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
task_3 = task.Task(name='Task C', description='This is desc from Task C', instruction='This is inst from Task C', sample_audio_name='file3.wav', created_user_id = 2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)
task_4 = task.Task(name='Task D', description='This is desc from Task D', instruction='This is inst from Task D', sample_audio_name='file4.wav', created_user_id = 2, created_at=TODAY_DATE_TIME, updated_at=TODAY_DATE_TIME)

db.session.add_all([task_1, task_2, task_3, task_4])
db.session.commit()

# create relationship between user and completed task
task_1.user_completed_tasks.append(user_1)
task_1.user_completed_tasks.append(user_2)
task_1.user_completed_tasks.append(user_3)
task_1.user_completed_tasks.append(user_4)
task_2.user_completed_tasks.append(user_1)
task_2.user_completed_tasks.append(user_3)
task_3.user_completed_tasks.append(user_1)

db.session.commit()


