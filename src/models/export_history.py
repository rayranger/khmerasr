from src import db
from datetime import datetime

class ExportHistory (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task_name = db.Column(db.String(), nullable=False)
    record_config_id = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    export_name = db.Column(db.String(), nullable=False)

    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))
    updated_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime("%d/%m/%Y_%H:%M:%S"))

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)