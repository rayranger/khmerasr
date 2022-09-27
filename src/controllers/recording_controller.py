from src.models import recording
from src import db

class RecordingController():
    
    def is_existed(self, data):
        req = recording.Recording.query.filter_by(id=data).first()
        req_1 = recording.Recording.query.filter_by(sample_filename=data).first()
        if req:
            return req
        elif req_1:
            return req_1
        else:
            return None
    
    def create_task_record(self, transcript, instruction, sample_filename, task_id):
        if self.is_existed(data=sample_filename):
            return None
        else:
            new_task_record = recording.Recording(
                transcript=transcript,
                instruction=instruction,
                sample_filename=sample_filename,
                task_id=task_id
            )
            db.session.add(new_task_record)
            db.session.commit()
            return new_task_record
    
    def update_task_record(self, new_task_record):
        task_record = self.is_existed(data=new_task_record.id)
        if task_record:
            task_record.transcript = new_task_record.transcript
            task_record.instruction = new_task_record.instruction
            task_record.sample_filename = new_task_record.sample_filename
            task_record.task_id = new_task_record.task_id 
            db.session.commit()
        else:
            return None
    
    def delete_task_record(self, id):
        task_record = self.is_existed(data=id)
        if task_record:
            db.session.delete(task_record)
            db.session.commit()
            return task_record
        else:
            return None
    
    def get_all_task_record(self):
        task_records = recording.TaskRecord.query.all()
        task_record_list = []
        for taskRecord in task_records:
            task_record_list.append(taskRecord)
        return task_record_list
