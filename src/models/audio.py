from src import db
from src.models.default_values import TODAY_DATE_TIME

class Audio(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(), nullable=False, unique=True)
    filetype = db.Column(db.String(), nullable=False)
    filesize = db.Column(db.Float(), nullable=False)
    channel = db.Column(db.Integer(), nullable=False)
    sample_rate = db.Column(db.Integer(), nullable=False)
    number_of_sample = db.Column(db.Integer(), nullable=False)
    total_frame = db.Column(db.Integer(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    speaker_id = db.Column(db.Integer(), db.ForeignKey('speaker.id'), nullable=False)
    recording_id = db.Column(db.Integer(), db.ForeignKey('recording.id'), nullable=False)


