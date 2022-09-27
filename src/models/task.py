from src import db
from sqlalchemy.orm import backref
from src.models.default_values import TODAY_DATE_TIME

class Task (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(length=500), nullable=True)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    from src.models import recording
    recordings = db.relationship('Recording', backref='task', lazy=True)
    created_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    record_config_id = db.Column(db.Integer(), db.ForeignKey('record_config.id'), nullable=True)