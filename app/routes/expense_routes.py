
from flask import Blueprint, request

from app.services.expense_service import (
    get_all_expenses,
    get_expense_by_id,
    create_expense,
    update_expense,
    delete_expense
)

from app.utils.validators import validate_expense_data
from app.utils.serializers import serialize_expense


expense_bp = Blueprint("expenses", __name__)


@expense_bp.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = get_all_expenses()

    return {
        "success": True,
        "count": len(expenses),
        "data": [
            serialize_expense(expense)
            for expense in expenses
        ]
    }, 200


@expense_bp.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    return {
        "success": True,
        "data": serialize_expense(expense)
    }, 200


@expense_bp.route("/expenses", methods=["POST"])
def post_expense():
    data = request.get_json(silent=True)

    validated_data, error = validate_expense_data(data)

    if error:
        return {"success": False, "error": error}, 400

    expense = create_expense(validated_data)

    return {
        "success": True,
        "message": "Expense created successfully",
        "id": expense.id
    }, 201


@expense_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def put_expense(expense_id):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    data = request.get_json(silent=True)

    validated_data, error = validate_expense_data(data)

    if error:
        return {"success": False, "error": error}, 400

    updated_expense = update_expense(expense, validated_data)

    return {
        "success": True,
        "message": "Expense updated successfully",
        "id": updated_expense.id
    }, 200


@expense_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def remove_expense(expense_id):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    delete_expense(expense)

    return {
        "success": True,
        "message": "Expense deleted successfully",
        "id": expense_id
    }, 200
