from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from flask_login import login_required
from app.camera.camera import generate_frames
from app.models import CameraSettings

camera = Blueprint('camera', __name__)

@camera.route('/camera')
@login_required
def cam():
    cameras = CameraSettings.get_all_cameras()
    return render_template('cam.html', cameras=cameras)

@camera.route('/video_feed/<int:camera_id>')
@login_required
def video_feed(camera_id):
    camera = CameraSettings.query.get_or_404(camera_id)
    return Response(generate_frames(camera.url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')