
from app.extensions import db
from app.models import Expense


def get_all_expenses():
    return db.session.execute(
        db.select(Expense).order_by(Expense.id)
    ).scalars().all()




def get_expense_by_id(expense_id):
    return db.session.get(Expense, expense_id)




def create_expense(data):
    expense = Expense(**data)

    db.session.add(expense)
    db.session.commit()

    return expense



def update_expense(expense, data):
    expense.amount = data["amount"]
    expense.category = data["category"]
    expense.date = data["date"]
    expense.description = data["description"]

    db.session.commit()

    return expense



def delete_expense(expense):
    db.session.delete(expense)
    db.session.commit()
