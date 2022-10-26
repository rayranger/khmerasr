from email.policy import default
from src import db, bcrypt, login_manager
from src.models.default_values import TODAY_DATE_TIME
from flask_login import UserMixin
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(id=user_id)
    return User.query.get(int(user_id))


user_role = db.Table ('user_role',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User (db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False, default="password_disable")
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    created_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)
    updated_at = db.Column(db.String(), nullable=False, default=TODAY_DATE_TIME)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    roles = db.relationship('Role', secondary=user_role, backref='users', lazy=True)
    speaker = db.relationship('Speaker', backref="user", lazy=True, uselist=False)
    tasks = db.relationship('Task', backref='created_by', lazy=True)