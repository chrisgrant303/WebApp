from flask import Blueprint, request, jsonify
from models.pto_holidays import PTOHoliday
from database import db

pto_holidays_blueprint = Blueprint('pto_holidays', __name__)

@pto_holidays_blueprint.route('/pto_holidays', methods=['POST'])
def add_pto_holiday():
    data = request.get_json()
    new_pto_holiday = PTOHoliday(resource_id=data['resource_id'], date=data['date'], pto_type=data['pto_type'], region=data.get('region', None))
    db.session.add(new_pto_holiday)
    db.session.commit()
    return jsonify({"message": "PTO/Holiday added successfully!"}), 201

@pto_holidays_blueprint.route('/pto_holidays', methods=['GET'])
def get_all_pto_holidays():
    pto_holidays = PTOHoliday.query.all()
    output = [{"id": pto.id, "resource_id": pto.resource_id, "date": pto.date, "pto_type": pto.pto_type, "region": pto.region} for pto in pto_holidays]
    return jsonify({"pto_holidays": output})

@pto_holidays_blueprint.route('/pto_holidays/<int:id>', methods=['PUT'])
def update_pto_holiday(id):
    pto_holiday = PTOHoliday.query.get(id)
    if not pto_holiday:
        return jsonify({"message": "PTO/Holiday not found!"}), 404

    data = request.get_json()
    pto_holiday.resource_id = data['resource_id']
    pto_holiday.date = data['date']
    pto_holiday.pto_type = data['pto_type']
    pto_holiday.region = data.get('region', None)
    db.session.commit()
    return jsonify({"message": "PTO/Holiday updated successfully!"})

@pto_holidays_blueprint.route('/pto_holidays/<int:id>', methods=['DELETE'])
def delete_pto_holiday(id):
    pto_holiday = PTOHoliday.query.get(id)
    if not pto_holiday:
        return jsonify({"message": "PTO/Holiday not found!"}), 404

    db.session.delete(pto_holiday)
    db.session.commit()
    return jsonify({"message": "PTO/Holiday deleted successfully!"})
