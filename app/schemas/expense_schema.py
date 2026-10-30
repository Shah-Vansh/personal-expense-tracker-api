from datetime import date
from decimal import Decimal

from pydantic import(
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

class ExpenseBaseSchema(BaseModel):
    model_config=ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    amount:Decimal=Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    category:str=Field(
        min_length=1,
        max_length=100,
    )

    date:date

    description:str | None=None

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Category cannot be empty")

        return value


class ExpenseCreateSchema(ExpenseBaseSchema):
    pass


class ExpenseUpdateSchema(ExpenseBaseSchema):
    pass


class ExpenseResponseSchema(ExpenseBaseSchema):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )

    id: int

class ExpenseFilterSchema(BaseModel):
    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    start_date: date | None = None
    end_date: date | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

    @model_validator(mode="after")
    def validate_date_range(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            raise ValueError(
                "start_date cannot be greater than end_date"
            )

        return self

class MonthlySummaryQuerySchema(BaseModel):
    year: int = Field(ge=2000, le=2100)
    month: int = Field(ge=1, le=12)
