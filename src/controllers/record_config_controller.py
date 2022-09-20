from src.models import record_config
from src import db

class RecordConfigController():

    def is_existed(self, data):
        req_1 = record_config.RecordConfig.query.filter_by(id=data).first()
        if req_1:
            return req_1
        else:
            return None
    
    def create_record_config(self, duration, frame_per_buffer, channel, rate):
        new_record_config = record_config.RecordConfig(
            duration=duration,
            frame_per_buffer=frame_per_buffer,
            channel=channel,
            rate=rate,
        )
        db.session.add(new_record_config)
        db.session.commit()
        return new_record_config
    
    def update_record_config(self, id, duration, frame_per_buffer, channel, rate):
        existing_record_config = self.is_existed(data=id)
        if existing_record_config:
            existing_record_config.duration = duration
            existing_record_config.frame_per_buffer = frame_per_buffer
            existing_record_config.channel = channel
            existing_record_config.rate = rate
            db.session.commit()
            return existing_record_config
        else:
            return None
    
    def delete_record_config(self, id):
        existing_record_config = self.is_existed(data=id)
        if existing_record_config:
            db.session.delete(existing_record_config)
            db.session.commit()
            return existing_record_config
        else:
            return None
    
    def get_all_record_config(self):
        record_configs = record_config.RecordConfig.query.all()
        record_config_list = []
        for recordConfig in record_configs:
            record_config_list.append(recordConfig)
        return record_config_list