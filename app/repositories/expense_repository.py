from sqlalchemy.orm import Session
from app.models.expense import Expense
from sqlalchemy import func
from datetime import date

class ExpenseRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Expense]:
        statement = (
            self.session.query(Expense)
            .order_by(Expense.id)
        )

        return statement.all()

    def get_by_id(self, expense_id: int) -> Expense | None:
        return self.session.get(Expense, expense_id)

    def create(self, data: dict) -> Expense:
        expense = Expense(**data)

        self.session.add(expense)
        self.session.flush()

        return expense

    def update(self, expense: Expense, data: dict) -> Expense:
        for field, value in data.items():
            setattr(expense, field, value)

        self.session.flush()

        return expense

    def delete(self, expense: Expense) -> None:
        self.session.delete(expense)
        self.session.flush()


    def get_filtered_expenses(
    self,
    category=None,
    start_date=None,
    end_date=None,
    page=1,
    limit=10
    ):
        query = self.session.query(Expense)

        if category is not None:
            query = query.filter(
                Expense.category == category
            )

        if start_date is not None:
            query = query.filter(
                Expense.date >= start_date
            )

        if end_date is not None:
            query = query.filter(
                Expense.date <= end_date
            )

        total = query.count()

        offset = (page - 1) * limit

        expenses = (
            query
            .order_by(Expense.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return expenses, total

    def get_monthly_summary(self, year, month):
        start_date = date(year, month, 1)

        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        results = (
            self.session.query(
                Expense.category,
                func.count(Expense.id).label("count"),
                func.sum(Expense.amount).label("total")
            )
            .filter(
                Expense.date >= start_date,
                Expense.date < end_date
            )
            .group_by(Expense.category)
            .order_by(Expense.category.asc())
            .all()
        )

        return results
