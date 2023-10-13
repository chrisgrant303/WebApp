from flask import Blueprint, request, jsonify
from models.release_schedule import ReleaseSchedule
from database import db

release_schedule_blueprint = Blueprint('release_schedule', __name__)

@release_schedule_blueprint.route('/release_schedule', methods=['POST'])
def add_release_schedule():
    data = request.get_json()
    new_schedule = ReleaseSchedule(release_name=data['release_name'], start_date=data['start_date'], end_date=data['end_date'])
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({"message": "Release Schedule added successfully!"}), 201

@release_schedule_blueprint.route('/release_schedule', methods=['GET'])
def get_all_release_schedules():
    schedules = ReleaseSchedule.query.all()
    output = [{"id": schedule.id, "release_name": schedule.release_name, "start_date": schedule.start_date, "end_date": schedule.end_date} for schedule in schedules]
    return jsonify({"release_schedules": output})

@release_schedule_blueprint.route('/release_schedule/<int:id>', methods=['PUT'])
def update_release_schedule(id):
    schedule = ReleaseSchedule.query.get(id)
    if not schedule:
        return jsonify({"message": "Release Schedule not found!"}), 404

    data = request.get_json()
    schedule.release_name = data['release_name']
    schedule.start_date = data['start_date']
    schedule.end_date = data['end_date']
    db.session.commit()
    return jsonify({"message": "Release Schedule updated successfully!"})

@release_schedule_blueprint.route('/release_schedule/<int:id>', methods=['DELETE'])
def delete_release_schedule(id):
    schedule = ReleaseSchedule.query.get(id)
    if not schedule:
        return jsonify({"message": "Release Schedule not found!"}), 404

    db.session.delete(schedule)
    db.session.commit()
    return jsonify({"message": "Release Schedule deleted successfully!"})
