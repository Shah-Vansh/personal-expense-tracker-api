from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Expense(db.Model):
    __tablename__="expenses"
    
    id=db.Column(db.Integer, db.Identity(always=True), primary_key=True)
    amount=db.Column(db.Numeric(10,2), nullable=False)
    category=db.Column(db.String(100), nullable=False)
    date=db.Column(db.Date, nullable=False)
    description=db.Column(db.Text, nullable=True)