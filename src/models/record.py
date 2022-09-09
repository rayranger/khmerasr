from src import db

class Record(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(), nullable=False, unique=True)
    filetype = db.Column(db.String(), nullable=False)
    filesize = db.Column(db.Float(), nullable=False)
    channel = db.Column(db.Integer(), nullable=False)
    sample_framerate = db.Column(db.Integer(), nullable=False)
    sample_frame = db.Column(db.Integer(), nullable=False)
    total_frame = db.Column(db.Integer(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    from src.models.speaker import Speaker
    speaker_id = db.Column(db.Integer(), db.ForeignKey('speaker.id'), nullable=False)
    from src.models.record_category import RecordCategory
    category_id = db.Column(db.Integer(), db.ForeignKey('record_category.id'), nullable=False)
