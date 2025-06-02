from flask import Blueprint, render_template
from flask_login import login_required
from app.models.settings import Settings
from datetime import datetime, timedelta
from app import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    settings = Settings.query.first()
    show_notification = False

    if settings and settings.next_notification_date:
        if settings.next_notification_date <= datetime.utcnow():
            show_notification = True

            if settings.notification_interval == 'week':
                settings.next_notification_date = datetime.utcnow() + timedelta(weeks=1)
            elif settings.notification_interval == '2weeks':
                settings.next_notification_date = datetime.utcnow() + timedelta(weeks=2)
            elif settings.notification_interval == 'month':
                settings.next_notification_date = datetime.utcnow() + timedelta(days=30)
            elif settings.notification_interval == '2months':
                settings.next_notification_date = datetime.utcnow() + timedelta(days=60)
            elif settings.notification_interval == 'custom' and settings.custom_days:
                settings.next_notification_date = datetime.utcnow() + timedelta(days=settings.custom_days)

            settings.last_notification = datetime.utcnow()
            db.session.commit()

    return render_template('index.html', show_notification=show_notification)

@main.route('/lights')
@login_required
def lights():
    return render_template('lights.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

