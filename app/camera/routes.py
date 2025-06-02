from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.camera.camera import generate_frames
from app.models import CameraSettings

camera = Blueprint('camera', __name__)

@camera.route('/camera')
@login_required
def cam():
    cameras = CameraSettings.query.filter_by(user_id=current_user.id).all()
    return render_template('cam.html', cameras=cameras)

@camera.route('/video_feed/<int:camera_id>')
@login_required
def video_feed(camera_id):
    camera = CameraSettings.query.filter_by(id=camera_id, user_id=current_user.id).first_or_404()
    return Response(
        generate_frames(
            camera.url,
            brightness=camera.brightness,
            contrast=camera.contrast
        ),
                    mimetype='multipart/x-mixed-replace; boundary=frame')