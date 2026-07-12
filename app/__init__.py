from flask import Flask

from app.config import Config
from app.services.database_service import close_db, init_database


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.clinical import clinical_bp
    from app.routes.public_health import public_health_bp
    from app.routes.patient_portal import patient_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clinical_bp)
    app.register_blueprint(public_health_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(admin_bp)

    app.teardown_appcontext(close_db)

    return app
