from src import db
from datetime import datetime

class Recording(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    transcript = db.Column(db.String(length=500), nullable=False)
    instruction = db.Column(db.String(length=500), nullable=False)
    sample_filename = db.Column(db.String(), nullable=True, unique=True)
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))


    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)
    audios = db.relationship('Audio', backref="recording", lazy=True)