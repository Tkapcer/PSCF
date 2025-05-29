from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')     

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'

    with app.app_context():
        from app.models import CameraSettings
        db.create_all()

    from app.auth.routes import auth
    from app.camera.routes import camera
    from app.main.routes import main
    from app.settings.routes import settings

    app.register_blueprint(auth)
    app.register_blueprint(camera)
    app.register_blueprint(main)
    app.register_blueprint(settings)

    return app