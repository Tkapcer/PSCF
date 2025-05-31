from app import db

class CameraSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    brightness = db.Column(db.Integer, default=0)
    contrast = db.Column(db.Float, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def get_settings():
        return CameraSettings.query.first()

    @classmethod
    def get_all_cameras(cls):
        return cls.query.all()