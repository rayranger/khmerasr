from src import db
from src.models.default_values import TODAY_DATE_TIME

class Recording(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    transcript = db.Column(db.String(length=500), nullable=False)
    instruction = db.Column(db.String(length=500), nullable=False)
    sample_filename = db.Column(db.String(), nullable=True, unique=True)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)


    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)
    audios = db.relationship('Audio', backref="recording", lazy=True)