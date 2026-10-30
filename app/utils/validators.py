
from datetime import date
from decimal import Decimal, InvalidOperation


def validate_expense_data(data):
    if not isinstance(data, dict):
        return None, "A JSON object is required"

    required_fields = ["amount", "category", "date"]

    for field in required_fields:
        if field not in data or data[field] is None:
            return None, f"{field} is required"

    try:
        if isinstance(data["amount"], bool):
            raise ValueError

        amount = Decimal(str(data["amount"]))

        if not amount.is_finite() or amount <= 0:
            raise ValueError

        if amount.as_tuple().exponent < -2:
            raise ValueError

        if amount >= 100000000:
            raise ValueError

    except (InvalidOperation, ValueError, TypeError):
        return None, "Invalid expense amount"

    category = data["category"]

    if not isinstance(category, str) or not category.strip():
        return None, "Category must be a non-empty string"

    category = category.strip()

    if len(category) > 100:
        return None, "Category cannot exceed 100 characters"

    if not isinstance(data["date"], str):
        return None, "Date must be in YYYY-MM-DD format"

    try:
        expense_date = date.fromisoformat(data["date"])

        if expense_date.isoformat() != data["date"]:
            raise ValueError

    except ValueError:
        return None, "Date must be in YYYY-MM-DD format"

    description = data.get("description")

    if description is not None and not isinstance(description, str):
        return None, "Description must be a string"

    validated_data = {
        "amount": amount,
        "category": category,
        "date": expense_date,
        "description": description
    }

    return validated_data, None
