from flask import current_app
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import HTTPException
from app.extensions import db
from app.exceptions.api_exceptions import APIException
from app.schemas.response_schema import ErrorDetailSchema
from app.utils.response_builder import ResponseBuilder

class ExceptionHandler:

    @staticmethod
    def register(app):

        @app.errorhandler(APIException)
        def handle_api_exception(error):
            return ResponseBuilder.error(
                message=error.message,
                code=error.error_code,
                status_code=error.status_code,
            )

        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            details = []

            for item in error.errors():
                field = ".".join(
                    str(part) for part in item["loc"]
                )

                details.append(
                    ErrorDetailSchema(
                        field=field,
                        message=item["msg"],
                    )
                )

            return ResponseBuilder.error(
                message="Request validation failed",
                code="VALIDATION_ERROR",
                status_code=422,
                details=details,
            )

        @app.errorhandler(OperationalError)
        def handle_database_error(error):
            db.session.rollback()

            current_app.logger.exception(
                "Database operation failed"
            )

            return ResponseBuilder.error(
                message="Database service unavailable",
                code="DATABASE_UNAVAILABLE",
                status_code=503,
            )

        @app.errorhandler(HTTPException)
        def handle_http_exception(error):
            return ResponseBuilder.error(
                message=error.description,
                code=error.name.upper().replace(" ", "_"),
                status_code=error.code or 500,
            )

        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            db.session.rollback()

            current_app.logger.exception(
                "Unexpected application error"
            )

            return ResponseBuilder.error(
                message="An unexpected error occurred",
                code="INTERNAL_SERVER_ERROR",
                status_code=500,
            )
