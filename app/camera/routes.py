from flask import Blueprint, render_template, Response, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.camera.camera import generate_frames
from app.models import CameraSettings
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


@camera.route('/camera/settings', methods=['GET', 'POST'])
@login_required
def camera_settings():
    settings = CameraSettings.get_settings()

    if request.method == 'POST':
        camera_url = request.form.get('camera_url')
        camera_name = request.form.get('camera_name')

        if settings:
            settings.url = camera_url
            settings.name = camera_name
        else:
            settings = CameraSettings(name=camera_name, url=camera_url)
            db.session.add(settings)

        db.session.commit()
        flash('Ustawienia kamery zostały zaktualizowane.', 'success')
        return redirect(url_for('camera.camera_settings'))

    return render_template('settings.html', settings=settings)
