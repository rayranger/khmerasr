from src import db
from src.models import export_history

class ExportHistoryController():

    def is_existed(self, data):
        req = export_history.ExportHistory.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None
    
    def create_export_history(self, task_name, record_config_id, gender, export_name, user_id):
        export_history_obj = export_history.ExportHistory(
            task_name=task_name,
            record_config_id=record_config_id,
            gender=gender,
            export_name=export_name,
            user_id=user_id
        )
        db.session.add(export_history_obj)
        db.session.commit()
        return export_history_obj
    
    def delete_export_history(self, id):
        req = self.is_existed(data=id)
        if req:
            db.session.delete(req)
            db.session.commit()
            return req
        else:
            return None
    
    def get_all_export_history(self):
        export_history_list = []
        export_histories = export_history.ExportHistory.query.all()
        for export_history_item in export_histories:
            export_history_list.append(export_history_item)
        return export_history_list
        
