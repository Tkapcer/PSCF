from app import db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    notification_interval = db.Column(db.String(20))
    custom_days = db.Column(db.Integer)
    last_notification = db.Column(db.DateTime)
    next_notification_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)