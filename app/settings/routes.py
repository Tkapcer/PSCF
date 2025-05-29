from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import CameraSettings
from app.settings import settings
from app import db

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    cameras = CameraSettings.get_all_cameras()

    if request.method == 'POST':
        camera_url = request.form.get('camera_url')
        camera_name = request.form.get('camera_name')

        new_camera = CameraSettings(name=camera_name, url=camera_url)
        db.session.add(new_camera)
        db.session.commit()
        flash('New camera has been added successfully.', 'success')
        return redirect(url_for('settings.settings_page'))

    return render_template('settings.html', cameras=cameras)

@settings.route('/settings/delete/<int:camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    camera = CameraSettings.query.get_or_404(camera_id)
    db.session.delete(camera)
    db.session.commit()
    flash('Camera has been deleted successfully.', 'success')
    return redirect(url_for('settings.settings_page'))