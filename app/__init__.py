
from flask import Flask

from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.models import Expense
    from app.routes.expense_routes import expense_bp

    app.register_blueprint(expense_bp)

    return app
