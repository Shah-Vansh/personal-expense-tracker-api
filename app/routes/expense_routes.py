from flask import Blueprint, request
from flask.views import MethodView
from app.extensions import db
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.schemas.expense_schema import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseResponseSchema,
    ExpenseFilterSchema,
)
from app.utils.response_builder import ResponseBuilder
from app.utils.request_parser import RequestParser
from app.schemas.expense_schema import MonthlySummaryQuerySchema

expense_bp = Blueprint("expenses", __name__)

class ExpenseBaseAPI(MethodView):

    def __init__(self):
        repository = ExpenseRepository(db.session)
        self.service = ExpenseService(repository)

    @staticmethod
    def serialize(expense):
        return ExpenseResponseSchema.model_validate(expense)

class ExpenseListAPI(ExpenseBaseAPI):

    def get(self):
        filters = ExpenseFilterSchema.model_validate(
            request.args.to_dict()
        )

        expenses, total = self.service.get_filtered_expenses(filters)

        expense_data = [
            self.serialize(expense)
            for expense in expenses
        ]

        total_pages = (
            total + filters.limit - 1
        ) // filters.limit

        return ResponseBuilder.success(
            message="Expenses retrieved successfully",
            data={
                "count": len(expense_data),
                "total": total,
                "page": filters.page,
                "limit": filters.limit,
                "total_pages": total_pages,
                "expenses": expense_data,
            },
        )

    def post(self):
        payload = ExpenseCreateSchema.model_validate(
            RequestParser.parse_json()
        )

        expense = self.service.create_expense(payload)

        return ResponseBuilder.success(
            message="Expense created successfully",
            data=self.serialize(expense),
            status_code=201,
        )

class ExpenseDetailAPI(ExpenseBaseAPI):

    def get(self, expense_id):
        expense = self.service.get_expense_by_id(
            expense_id
        )

        return ResponseBuilder.success(
            message="Expense retrieved successfully",
            data=self.serialize(expense),
        )

    def put(self, expense_id):
        payload = ExpenseUpdateSchema.model_validate(
            RequestParser.parse_json()
        )

        expense = self.service.update_expense(
            expense_id,
            payload,
        )

        return ResponseBuilder.success(
            message="Expense updated successfully",
            data=self.serialize(expense),
        )

    def delete(self, expense_id):
        self.service.delete_expense(expense_id)

        return ResponseBuilder.success(
            message="Expense deleted successfully",
        )


class MonthlyExpenseSummaryAPI(ExpenseBaseAPI):

    def get(self):
        query_params = MonthlySummaryQuerySchema.model_validate(
            request.args.to_dict()
        )

        summary = self.service.get_monthly_summary(
            year=query_params.year,
            month=query_params.month
        )

        return ResponseBuilder.success(
            message="Monthly expense summary retrieved successfully",
            data=summary
        )


expense_list_view = ExpenseListAPI.as_view(
    "expense_list"
)

expense_detail_view = ExpenseDetailAPI.as_view(
    "expense_detail"
)

expense_bp.add_url_rule(
    "/expenses",
    view_func=expense_list_view,
    methods=["GET", "POST"],
)

expense_bp.add_url_rule(
    "/expenses/<int:expense_id>",
    view_func=expense_detail_view,
    methods=["GET", "PUT", "DELETE"],
)

expense_bp.add_url_rule(
    "/expenses/summary/monthly",
    view_func=MonthlyExpenseSummaryAPI.as_view(
        "monthly_expense_summary"
    )
)
