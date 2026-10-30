from app.extensions import db
from app.models import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.exceptions.api_exceptions import ResourceNotFoundException
from decimal import Decimal

class ExpenseService:

    def __init__(self, repository: ExpenseRepository):
        self.repository = repository

    def get_all_expenses(self):
        return self.repository.get_all()

    def get_expense_by_id(self, expense_id: int):
        expense = self.repository.get_by_id(expense_id)

        if expense is None:
            raise ResourceNotFoundException(
                "Expense not found"
            )

        return expense

    def create_expense(self, data):
        session = self.repository.session

        try:
            expense = self.repository.create(
                data.model_dump()
            )

            session.commit()
            session.refresh(expense)

            return expense

        except Exception:
            session.rollback()
            raise

    def update_expense(self, expense_id: int, data):
        session = self.repository.session

        try:
            expense = self.get_expense_by_id(expense_id)

            updated_expense = self.repository.update(
                expense,
                data.model_dump()
            )

            session.commit()
            session.refresh(expense)

            return updated_expense

        except Exception:
            session.rollback()
            raise

    def delete_expense(self, expense_id: int):
        session = self.repository.session

        try:
            expense = self.get_expense_by_id(expense_id)

            self.repository.delete(expense)

            session.commit()

        except Exception:
            session.rollback()
            raise

    def get_filtered_expenses(self, filters):
        expenses, total = self.repository.get_filtered_expenses(
            category=filters.category,
            start_date=filters.start_date,
            end_date=filters.end_date,
            page=filters.page,
            limit=filters.limit
        )

        return expenses, total

    def get_monthly_summary(self, year, month):
        results = self.repository.get_monthly_summary(
            year=year,
            month=month
        )
        categories = []
        monthly_total = Decimal("0.00")
        transaction_count = 0

        for row in results:
            category_total = row.total

            categories.append({
                "category": row.category,
                "count": row.count,
                "total": str(category_total)
            })

            monthly_total += category_total
            transaction_count += row.count

        return {
            "year": year,
            "month": month,
            "total": str(monthly_total),
            "transaction_count": transaction_count,
            "categories": categories
        }
