class APIException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class ResourceNotFoundException(APIException):

    def __init__(self, message="Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class DatabaseUnavailableException(APIException):

    def __init__(self):
        super().__init__(
            message="Database service unavailable",
            status_code=503,
            error_code="DATABASE_UNAVAILABLE",
        )


class BadRequestException(APIException):

    def __init__(self, message="Invalid request"):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST",
        )
