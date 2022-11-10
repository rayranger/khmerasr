from src import db
from datetime import datetime

class Speaker(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    occupation = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    records = db.relationship('Audio', backref='speaker', lazy=True)