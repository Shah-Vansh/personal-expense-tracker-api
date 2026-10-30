from flask import request
from app.exceptions.api_exceptions import BadRequestException

class RequestParser:

    @staticmethod
    def parse_json():
        if not request.is_json:
            raise BadRequestException(
                "Content-Type must be application/json"
            )

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            raise BadRequestException(
                "Request body must be a valid JSON object"
            )

        return data
