from flask import Flask, request
import os
from dotenv import load_dotenv
from models import db, Expense
from datetime import date
from decimal import Decimal, InvalidOperation

load_dotenv()
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
db.init_app(app)

@app.route("/",methods=["GET"])
def home():
    return {"message":"Personal Expense Tracker API is running"}


@app.route("/db-test",methods=["GET"])
def database_test():
    with app.app_context():
        result=db.session.execute(db.text("SELECT current_database()"))
        database_name=result.scalar()    
    return{"database":database_name}


@app.route("/expenses-test",methods=["GET"])
def expense_test():
    expenses=db.session.execute(
        db.select(Expense)
    ).scalars().all()
    
    return{
        "count":len(expenses),
        "expenses":[
            {
                "id": expense.id,
                "amount": str(expense.amount),
                "category": expense.category,
                "date": expense.date.isoformat(),
                "description": expense.description
            }
            for expense in expenses
        ]
    }
    
    
@app.route("/expenses",methods=["GET"])
def get_expenses():
    expenses = db.session.execute(
        db.select(Expense).order_by(Expense.id)
    ).scalars().all()

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "amount": str(expense.amount),
            "category": expense.category,
            "date": expense.date.isoformat(),
            "description": expense.description
        })

    return {
        "success": True,
        "count": len(result),
        "data": result
    }, 200

@app.route("/expenses",methods=["POST"])
def create_expense():
    data=request.get_json(silent=True)
    
    if not isinstance(data, dict):
        return {"error":"A JSON object is required"},400
    
    required_fields=["amount","category","date"]
    
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"error":f"{field} is required"},400
    
    try:
        if isinstance(data["amount"], bool):
            raise ValueError
    
        amount=Decimal(str(data["amount"])) 
        
        if not amount.is_finite() or amount <= 0:
                raise ValueError

        if amount.as_tuple().exponent < -2 or amount >= 100000000:
            raise ValueError   
    
    except (InvalidOperation, ValueError, TypeError):
        return {"error": "Invalid expense amount"}, 400

    category = data["category"]

    if not isinstance(category, str) or not category.strip():
        return {"error": "Category must be a non-empty string"}, 400

    category = category.strip()

    if len(category) > 100:
        return {"error": "Category cannot exceed 100 characters"}, 400

    try:
        expense_date = date.fromisoformat(data["date"])
    except (ValueError, TypeError):
        return {"error": "Date must be in YYYY-MM-DD format"}, 400

    description = data.get("description")

    if description is not None and not isinstance(description, str):
        return {"error": "Description must be a string"}, 400

    expense = Expense(
        amount=amount,
        category=category,
        date=expense_date,
        description=description
    )

    db.session.add(expense)
    db.session.commit()

    return {
        "success": True,
        "message": "Expense created successfully",
        "id": expense.id
    }, 201




@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    return {
        "success": True,
        "data": {
            "id": expense.id,
            "amount": str(expense.amount),
            "category": expense.category,
            "date": expense.date.isoformat(),
            "description": expense.description
        }
    }, 200
    
    

@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "A JSON object is required"}, 400

    required_fields = ["amount", "category", "date"]

    for field in required_fields:
        if field not in data or data[field] is None:
            return {"error": f"{field} is required"}, 400

    try:
        if isinstance(data["amount"], bool):
            raise ValueError

        amount = Decimal(str(data["amount"]))

        if not amount.is_finite() or amount <= 0:
            raise ValueError

        if amount.as_tuple().exponent < -2 or amount >= 100000000:
            raise ValueError

    except (InvalidOperation, ValueError, TypeError):
        return {"error": "Invalid expense amount"}, 400

    category = data["category"]

    if not isinstance(category, str) or not category.strip():
        return {"error": "Category must be a non-empty string"}, 400

    category = category.strip()

    if len(category) > 100:
        return {"error": "Category cannot exceed 100 characters"}, 400

    try:
        expense_date = date.fromisoformat(data["date"])
    except (ValueError, TypeError):
        return {"error": "Date must be in YYYY-MM-DD format"}, 400

    description = data.get("description")

    if description is not None and not isinstance(description, str):
        return {"error": "Description must be a string"}, 400

    expense.amount = amount
    expense.category = category
    expense.date = expense_date
    expense.description = description

    db.session.commit()

    return {
        "success": True,
        "message": "Expense updated successfully",
        "id": expense.id
    }, 200




@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        return {
            "success": False,
            "message": "Expense not found"
        }, 404

    db.session.delete(expense)
    db.session.commit()

    return {
        "success": True,
        "message": "Expense deleted successfully",
        "id": expense_id
    }, 200


if __name__=="__main__":
    app.run(debug=True)