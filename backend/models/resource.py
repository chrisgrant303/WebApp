from datetime import datetime
from database import db
from models.group import Group


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    total_time = db.Column(db.Float, nullable=False)
    forecasted_cost = db.Column(db.Float, nullable=False)
    monthly_hours = db.Column(db.Text, nullable=True)  # We'll store this as JSON for flexibility
