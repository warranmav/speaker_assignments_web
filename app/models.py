from app import db

# Record Table (Existing Table)
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    exception = db.Column(db.String(20), nullable=True)


    # Relationship to TalkAssignment
    assignments = db.relationship('TalkAssignment', backref='speaker', lazy=True)

# New Table: TalkAssignment
class TalkAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    speaker_pos = db.Column(db.String(50), nullable=False)
    talk_length = db.Column(db.String(20), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)

# New Table: Theme
class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    topics = db.relationship('Topic', backref='theme', lazy=True)

# New Table: Topic
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
