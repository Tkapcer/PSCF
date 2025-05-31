from calendar import month
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from win32trace import flush

from app.models import CameraSettings, Settings
from app.settings import settings
from app import db

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    cameras = CameraSettings.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        camera_url = request.form.get('camera_url')
        camera_name = request.form.get('camera_name')


        new_camera = CameraSettings(name=camera_name, url=camera_url, user_id=current_user.id)
        db.session.add(new_camera)
        db.session.commit()
        flash('New camera has been added successfully.', 'success')
        return redirect(url_for('settings.settings_page'))

    settings_data = Settings.query.first()
    return render_template('settings.html',
                           cameras=cameras,
                           saved_temperature=settings_data.temperature if settings_data else None,
                           saved_interval=settings_data.notification_interval if settings_data else None,
                           saved_custom_days=settings_data.custom_days if settings_data else None)

@settings.route('/video_settings/<int:camera_id>', methods=['POST'])
@login_required
def video_settings(camera_id):

    try:
        brightness = int(request.form.get('brightness'))
        contrast = float(request.form.get('contrast'))
    except ValueError:
        brightness = 0
        contrast = 0
        flush("Invalid input for brightness or contrast", "error")
        redirect(url_for('settings.settings_page'))

    camera = CameraSettings.query.get_or_404(camera_id)

    if camera.user_id != current_user.id:
        abort(403)

    camera.brightness = brightness
    camera.contrast = contrast

    db.session.commit()
    flash('New video settings of camera has been updated.', 'success')
    return redirect(url_for('settings.settings_page'))

@settings.route('/settings/delete/<int:camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    camera = CameraSettings.query.get_or_404(camera_id)

    if camera.user_id != current_user.id:
        abort(403)

    db.session.delete(camera)
    db.session.commit()
    flash('Camera has been deleted successfully.', 'success')
    return redirect(url_for('settings.settings_page'))

from datetime import datetime, timedelta

@settings.route('/save_temperature', methods=['POST'])
@login_required
def save_temperature():
    temperature = float(request.form['temperature'])
    
    settings = Settings.query.first() or Settings()
    settings.temperature = temperature
    db.session.add(settings)
    db.session.commit()
    
    flash('Temperature saved successfully!', 'success')
    return redirect(url_for('settings.settings_page'))
    

@settings.route('/save_notifications', methods=['POST'])
@login_required
def save_notifications():
    interval = request.form['notification_interval']
    custom_days = int(request.form.get('custom_days', 0)) if interval == 'custom' else None
    
    settings = Settings.query.first() or Settings()
    settings.notification_interval = interval
    settings.custom_days = custom_days
    
    if interval == 'week':
        settings.next_notification_date = datetime.utcnow() + timedelta(weeks=1)
    elif interval == '2weeks':
        settings.next_notification_date = datetime.utcnow() + timedelta(weeks=2)
    elif interval == 'month':
        settings.next_notification_date = datetime.utcnow() + timedelta(days=30)
    elif interval == '2months':
        settings.next_notification_date = datetime.utcnow() + timedelta(days=60)
    elif interval == 'custom' and custom_days:
        settings.next_notification_date = datetime.utcnow() + timedelta(days=custom_days)

    db.session.add(settings)
    db.session.commit()
    flash('Notification settings saved!', 'success')
    return redirect(url_for('settings.settings_page'))

def check_notifications():
    now = datetime.utcnow()
    settings = Settings.query.first()

    if settings and settings.next_notification_date and Settings.next_notification_date <= now:
       # send_notification()
        
        Settings.next_notification_date = now + timedelta(days=Settings.notification_interval_days)
        db.session.commit()