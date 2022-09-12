from src import db
from src.models.default_values import TODAY_DATE_TIME

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
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    from src.models.user import User
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    records = db.relationship('Record', backref='speaker', lazy=True, cascade="all,delete")