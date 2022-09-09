from src import db

class RecordCategory(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=False)

    records = db.relationship('Record', backref='record_category', lazy=True)

    # def __repr__(self):
    #     return ({
    #         'id':self.id,
    #         'name':self.name,
    #         'created_at':self.created_at,
    #         'updated_at':self.updated_at
    #     })