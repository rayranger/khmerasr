from src import db
from src.models.default_values import TODAY_DATE_TIME

class RecordConfig(db.Model):
    pass
    id = db.Column(db.Integer(), primary_key=True)
    duration = db.Column(db.Integer(), nullable=True, default=3)
    number_of_sample = db.Column(db.Integer(), nullable=False, default=3200)
    channel = db.Column(db.Integer(), nullable=False, default=1)
    sample_rate = db.Column(db.Integer(), nullable=False, default = 16000)
    filetype = db.Column(db.String(), nullable=False, default = 'wav')
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    
    tasks = db.relationship('Task', backref='record_config', lazy=True)