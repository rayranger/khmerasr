from unicodedata import name
from src import db
from src.models import audio, record_category, role, speaker, user, record_config, task

# print(record_category.RecordCategory.query.all())
# print(record_config.RecordConfig.query.all())
# print(record.Record.query.all())
# print(role.Role.query.all())
# print(speaker.Speaker.query.all())
# print(task.Task.query.all())
# print(user.User.query.all())

# users = user.User.query.all()
# for user in users:
#     print(f'speaker name: {user.speaker.first_name}')
#     roles = user.roles
#     for role in roles:
#         print(f'{user.username} role as {role.name}')
#     tasks = user.tasks
#     for task in tasks:
#         print(f'This user assigned tasks: {task.name}')
#     completed_tasks = user.completed_tasks
#     for completed_task in completed_tasks:
#         print(f'This user completed task: {completed_task.name}')

#     print('-----------')

users = user.User.query.all()
print(users.to_json())