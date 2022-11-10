from src import db
from sqlalchemy.orm import backref
from datetime import datetime

class Task (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(length=500), nullable=True)
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))

    from src.models import recording
    recordings = db.relationship('Recording', backref='task', lazy=True)
    created_user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    record_config_id = db.Column(db.Integer(), db.ForeignKey('record_config.id'), nullable=True)