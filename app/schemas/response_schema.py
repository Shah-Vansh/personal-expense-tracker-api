from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetailSchema(BaseModel):
    field: str | None = None
    message: str

class ErrorSchema(BaseModel):
    code: str
    details: list[ErrorDetailSchema] | None = None

class APIResponseSchema(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    error: ErrorSchema | None = None
