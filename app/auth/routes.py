from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.models.schedule import Schedule
from app.models.area import Area
from flask import jsonify

auth = Blueprint('auth', __name__)
bp = Blueprint('schedule', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Nieprawidłowa nazwa użytkownika lub hasło')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Ta nazwa użytkownika jest już zajęta')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Ten email jest już używany')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Rejestracja udana! Możesz się teraz zalogować')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/save_schedules', methods=['POST'])
def save_schedules():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if 'schedules' not in data:
            return jsonify({"error": "Missing schedules key"}), 400

        db.session.begin()

        Area.query.delete()
        Schedule.query.delete()

        for sched in data['schedules']:
            if not all(k in sched for k in ['start_time', 'end_time', 'repeat_days', 'enabled', 'areas']):
                db.session.rollback()
                return jsonify({"error": "Invalid schedule format"}), 400

            schedule = Schedule(
                start_time=sched['start_time'],
                end_time=sched['end_time'],
                repeat_days=','.join(sched['repeat_days']),
                enabled=sched['enabled']
            )
            db.session.add(schedule)
            db.session.flush()

            for area in sched['areas']:
                if not all(k in area for k in ['color', 'intensity']):
                    db.session.rollback()
                    return jsonify({"error": "Invalid area format"}), 400

                a = Area(
                    schedule_id=schedule.id,
                    color=area['color'],
                    intensity=area['intensity']
                )
                db.session.add(a)

        db.session.commit()
        return jsonify({"status": "ok", "saved": len(data['schedules'])}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route('/get_schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.options(db.joinedload(Schedule.areas)).all()

    result = []
    for sched in schedules:
        result.append({
            'start_time': str(sched.start_time),
            'end_time': str(sched.end_time),
            'repeat_days': sched.repeat_days.split(','),
            'enabled': bool(sched.enabled),
            'areas': [{
                'color': area.color,
                'intensity': int(area.intensity)
            } for area in sched.areas]
        })

    return jsonify(result)


########PROFILE

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@auth.route('/get_profile', methods=['GET'])
@login_required
def get_profile():
    try:
        user = current_user
        return jsonify({
            'success': True,
            'email': user.email,
            'username': user.username
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@auth.route('/save_profile', methods=['POST'])
@login_required
def save_profile():
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': 'Request must be JSON'
            }), 400

        data = request.get_json()
        user = current_user

        # Walidacja email - sprawdź czy nie jest już używany przez innego użytkownika
        if 'email' in data and data['email']:
            existing_user = User.query.filter(
                User.email == data['email'],
                User.id != user.id
            ).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Ten email jest już używany przez innego użytkownika'
                }), 400

        # Walidacja hasła
        if data.get('new_password'):
            if not data.get('confirm_password'):
                return jsonify({
                    'success': False,
                    'message': 'Potwierdź nowe hasło'
                }), 400

            if data['new_password'] != data['confirm_password']:
                return jsonify({
                    'success': False,
                    'message': 'Hasła nie są identyczne'
                }), 400

            if len(data['new_password']) < 6:
                return jsonify({
                    'success': False,
                    'message': 'Hasło musi mieć co najmniej 6 znaków'
                }), 400

        # Aktualizuj dane użytkownika
        if 'email' in data and data['email']:
            user.email = data['email']

        if data.get('new_password'):
            user.set_password(data['new_password'])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profil został zaktualizowany pomyślnie'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Wystąpił błąd: {str(e)}'
        }), 500