from app import db

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    exception = db.Column(db.String(20), nullable=True)
    included_in_pool = db.Column(db.Boolean, default=True)
    date_last_spoken = db.Column(db.Date, nullable=True)
    speaker_pos = db.Column(db.String(50), nullable=True)
    talk_length = db.Column(db.String(20), nullable=True)
