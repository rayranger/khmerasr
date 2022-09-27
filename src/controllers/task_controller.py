from src.models import task
from src import db

class TaskController():

    def is_existed(self, data):
        req_1 = task.Task.query.filter_by(id=data).first()
        req_2 = task.Task.query.filter_by(name=data).first()
        if req_1 or req_2:
            return req_1
        else:
            return None
    
    def create_task(self, name, description, created_user_id, record_config_id):
        if self.is_existed(data=name):
            return None
        else:
            new_task = task.Task(
                name=name,
                description=description,
                created_user_id=created_user_id,
                record_config_id = record_config_id
            )
            db.session.add(new_task),
            db.session.commit()
            return new_task
    
    def update_task(self, new_task_obj):
        task_obj = self.is_existed(data=new_task_obj.id)
        if task_obj:
            task_obj.name = new_task_obj.name
            task_obj.description = new_task_obj.descrption
            task_obj.created_user_id = new_task_obj.created_user_id
            task_obj.record_config_id = new_task_obj.record_config_id
            db.session.commit()
            return new_task_obj
        else:
            return None
    
    def delete_taskr(self, id):
        task_obj = self.is_existed(data=id)
        if task_obj:
            db.session.delete(task_obj)
            db.session.commit()
            return task_obj
        else:
            return None
    
    def get_all_task(self):
        tasks = task.Task.query.all()
        taskList = []
        for taskItem in tasks:
            taskList.append(taskItem)
        return taskList