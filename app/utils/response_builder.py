from typing import Any
from flask import jsonify
from app.schemas.response_schema import (
    APIResponseSchema,
    ErrorSchema,
    ErrorDetailSchema,
)


class ResponseBuilder:

    @staticmethod
    def success(
        message: str,
        data: Any = None,
        status_code: int = 200,
    ):
        response = APIResponseSchema[Any](
            success=True,
            message=message,
            data=data,
            error=None,
        )

        return jsonify(
            response.model_dump(mode="json")
        ), status_code

    @staticmethod
    def error(
        message: str,
        code: str,
        status_code: int,
        details: list[ErrorDetailSchema] | None = None,
    ):
        response = APIResponseSchema[Any](
            success=False,
            message=message,
            data=None,
            error=ErrorSchema(
                code=code,
                details=details,
            ),
        )

        return jsonify(
            response.model_dump(mode="json")
        ), status_code
