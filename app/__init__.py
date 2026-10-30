from flask import Flask

from app.config import Config
from app.extensions import db, migrate
from app.exceptions.handlers import ExceptionHandler


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    from app.models import Expense

    migrate.init_app(app, db)
    ExceptionHandler.register(app)

    from app.routes.expense_routes import expense_bp
    app.register_blueprint(expense_bp)

    return app
