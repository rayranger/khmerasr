from asyncio import FastChildWatcher
from src import db

class RecordConfig (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    duration = db.Column(db.Integer(), nullable=False)
    frame_per_buffer = db.Column(db.Integer(), nullable=False)
    channel = db.Column(db.Integer(), nullable=False)
    rate = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    from src.models import user
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)