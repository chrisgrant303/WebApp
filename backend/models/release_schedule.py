from database import db

class ReleaseSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(120), nullable=False)
    hours = db.Column(db.Integer, nullable=False)

