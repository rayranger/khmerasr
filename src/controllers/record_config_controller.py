from src.models import record_config
from datetime import datetime
from src import db

class RecordConfigController():

    # Check by id
    def is_existed(self, data):
        req = record_config.RecordConfig.query.filter_by(id=data).first()
        if req:
            return req
        else:
            return None
    
    def create_record_config(self, duration, number_of_sample, channel, sample_rate, filetype):
        new_record_config = record_config.RecordConfig(
            duration=duration,
            number_of_sample=number_of_sample,
            channel=channel,
            sample_rate=sample_rate,
            filetype=filetype
        )
        db.session.add(new_record_config)
        db.session.commit()
        return new_record_config
    
    def update_record_config(self, id, duration, number_of_sample, channel, sample_rate, filetype):
        existing_record_config = self.is_existed(data=id)
        if existing_record_config:
            existing_record_config.duration = duration
            existing_record_config.number_of_sample = number_of_sample
            existing_record_config.channel = channel
            existing_record_config.sample_rate = sample_rate
            existing_record_config.filetype = filetype
            existing_record_config.updated_at = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
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