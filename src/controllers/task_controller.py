from src.models import task
from datetime import datetime
from src import db
from sqlalchemy import desc, asc

class TaskController():

    # Check by name
    def is_existed(self, data):
        req = task.Task.query.filter_by(name=data).first()
        if req:
            return req
        return None
    
    # Check by id
    def findTaskById(self, data):
        req = task.Task.query.filter_by(id=data).first()
        if req:
            return req
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
    
    def update_task(self, new_task_obj, id):
        task_obj = self.findTaskById(data=id)
        if task_obj:
            task_obj.name = new_task_obj.name
            task_obj.description = new_task_obj.description
            task_obj.created_user_id = new_task_obj.created_user_id
            task_obj.record_config_id = new_task_obj.record_config_id
            task_obj.updated_at = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            db.session.commit()
            return new_task_obj
        else:
            return None
    
    def delete_taskr(self, id):
        task_obj = self.findTaskById(data=id)
        print(task_obj)
        if task_obj:
            db.session.delete(task_obj)
            db.session.commit()
            return task_obj
        else:
            return None
    
    def get_all_task(self):
        # tasks = task.Task.query.all()
        tasks = task.Task.query.order_by(asc(task.Task.id))
        taskList = []
        for taskItem in tasks:
            taskList.append(taskItem)
        print(tasks)
        return taskList