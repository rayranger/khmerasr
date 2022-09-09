from src import db
from src.models import role
from src.models.default_values import TODAY_DATE_TIME

user_role = db.Table ('user_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    roles = db.relationship('Role', secondary=user_role, backref='users', lazy=True)
    speaker = db.relationship('Speaker', backref='user', lazy=True, uselist=False)
    config = db.relationship('RecordConfig', backref='config_owner', lazy=True, uselist=False)
    tasks = db.relationship('Task', backref='created_by', lazy=True)