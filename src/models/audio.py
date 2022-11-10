from src import db
from datetime import datetime

class Audio(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(), nullable=False, unique=True)
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))

    speaker_id = db.Column(db.Integer(), db.ForeignKey('speaker.id'), nullable=False)
    recording_id = db.Column(db.Integer(), db.ForeignKey('recording.id'), nullable=False)


