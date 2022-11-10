from src import db
from datetime import datetime

class RecordConfig(db.Model):
    pass
    id = db.Column(db.Integer(), primary_key=True)
    duration = db.Column(db.Integer(), nullable=True, default=3)
    number_of_sample = db.Column(db.Integer(), nullable=False, default=3200)
    channel = db.Column(db.Integer(), nullable=False, default=1)
    sample_rate = db.Column(db.Integer(), nullable=False, default = 16000)
    filetype = db.Column(db.String(), nullable=False, default = 'wav')
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    
    tasks = db.relationship('Task', backref='record_config', lazy=True)