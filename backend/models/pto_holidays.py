from database import db

class PTOHoliday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    pto_type = db.Column(db.String(50), nullable=False)  # PTO or Holiday
    region = db.Column(db.String(50), nullable=True)  # Only for holidays
