import os

import pytest
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

from app import create_app
from app.extensions import db


load_dotenv()


@pytest.fixture
def app():
    test_url = os.environ.get("TEST_DATABASE_URL")

    if not test_url:
        pytest.fail("TEST_DATABASE_URL is required for testing")

    url = make_url(test_url)

    if (
        url.database != "expense_tracker_test"
        or url.host not in ("localhost", "127.0.0.1")
    ):
        pytest.fail("Unsafe test database configuration")

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": test_url,
    })

    with app.app_context():

        actual_url = make_url(str(db.engine.url))

        if actual_url.database != "expense_tracker_test":
            pytest.fail("Flask connected to the wrong database")

        db.create_all()

        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
