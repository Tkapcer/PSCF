import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'super_tajne'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    RTSP_URL = 'rtsp://testpscf:bajojajo@192.168.1.31:554/stream1'