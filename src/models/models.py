from src import db

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
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    # from src.models.role import Role
    roles = db.relationship('Role', secondary=user_role, backref='users')
    # from src.models.speaker import Speaker
    speaker = db.relationship('Speaker', backref='user')

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

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
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    # from src.models.user import User
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    # from src.models.record import Record
    records = db.relationship('Record', backref='speaker', lazy=True)

class RecordCategory(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    # from src.models.record import Record
    records = db.relationship('Record', backref='record_category', lazy=True)

class Record(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(), nullable=False, unique=True)
    file_type = db.Column(db.String(), nullable=False)
    file_size = db.Column(db.Float(), nullable=False)
    channel = db.Column(db.Integer(), nullable=False)
    sample_framerate = db.Column(db.Integer(), nullable=False)
    sample_frame = db.Column(db.Integer(), nullable=False)
    total_frame = db.Column(db.Integer(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    # from src.models.speaker import Speaker
    speaker_id = db.Column(db.Integer(), db.ForeignKey('speaker.id'), nullable=False)
    # from src.models.record_category import RecordCategory
    category_id = db.Column(db.Integer(), db.ForeignKey('record_category.id'), nullable=False)