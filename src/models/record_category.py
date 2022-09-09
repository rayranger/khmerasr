from src import db
from src.models.default_values import TODAY_DATE_TIME

class RecordCategory(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    records = db.relationship('Record', backref='record_category', lazy=True)
