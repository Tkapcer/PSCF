from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from flask_login import login_required
from app.camera.camera import generate_frames
from config import Config

camera = Blueprint('camera', __name__)

@camera.route('/camera')
@login_required
def cam():
    return render_template('cam.html')

@camera.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')