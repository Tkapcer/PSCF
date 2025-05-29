from app import db

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    repeat_days = db.Column(db.String(100))
    enabled = db.Column(db.Boolean)

    areas = db.relationship('Area', backref='schedule', cascade='all, delete-orphan')