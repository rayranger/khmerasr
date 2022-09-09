from src import db

user_completed_task = db.Table ('user_completed_task',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
)

class Task (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(length=500), nullable=True)
    instruction = db.Column(db.String(length=500), nullable=False)
    sample_audio_name = db.Column(db.String(), nullable=True, unique=True)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    from src.models import user
    created_user_id = db.Column(db.String(), db.ForeignKey('user.id'), nullable=False)
    user_completed_tasks = db.relationship('User', secondary=user_completed_task, backref="completed_tasks", lazy=True)

