from database import db

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial_budget = db.Column(db.Float, nullable=False)
    adjustments = db.Column(db.Text, nullable=True)  # Storing as JSON for flexibility
