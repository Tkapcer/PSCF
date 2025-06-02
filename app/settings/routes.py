from calendar import month
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import CameraSettings, Settings
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

    settings_data = Settings.query.first()
    return render_template('settings.html',
                           cameras=cameras,
                           saved_temperature=settings_data.temperature if settings_data else None,
                           saved_interval=settings_data.notification_interval if settings_data else None,
                           saved_custom_days=settings_data.custom_days if settings_data else None)

@settings.route('/settings/delete/<int:camera_id>', methods=['POST'])
@login_required
def delete_camera(camera_id):
    camera = CameraSettings.query.get_or_404(camera_id)
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
    #settings.next_notification_date = datetime.utcnow() - timedelta(minutes=1)

    db.session.commit()
    flash('Notification settings saved!', 'success')
    return redirect(url_for('settings.settings_page'))
