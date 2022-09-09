from src import db
from src.models.default_values import TODAY_DATE_TIME

class RecordConfig (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    duration = db.Column(db.Integer(), nullable=False, default=3)
    frame_per_buffer = db.Column(db.Integer(), nullable=False, default=3200)
    channel = db.Column(db.Integer(), nullable=False, default=1)
    rate = db.Column(db.Integer(), nullable=False, default = 16000)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    from src.models import user
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)