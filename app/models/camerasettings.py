from app import db

class CameraSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False)

    @staticmethod
    def get_settings():
        return CameraSettings.query.first()

    @classmethod
    def get_all_cameras(cls):
        return cls.query.all()