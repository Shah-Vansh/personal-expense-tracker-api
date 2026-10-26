def serialize_expense(expense):
    return {
        "id": expense.id,
        "amount": str(expense.amount),
        "category": expense.category,
        "date": expense.date.isoformat(),
        "description": expense.description
    }
