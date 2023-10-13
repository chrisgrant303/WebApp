from flask import Blueprint, request, jsonify
from models.group import Group
from database import db

group_blueprint = Blueprint('group', __name__)

@group_blueprint.route('/group', methods=['POST'])
def add_group():
    data = request.get_json()
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group added successfully!"}), 201

@group_blueprint.route('/group', methods=['GET'])
def get_all_groups():
    groups = Group.query.all()
    output = [{"id": group.id, "name": group.name} for group in groups]
    return jsonify({"groups": output})

@group_blueprint.route('/group/<int:id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get(id)
    if not group:
        return jsonify({"message": "Group not found!"}), 404

    data = request.get_json()
    group.name = data['name']
    db.session.commit()
    return jsonify({"message": "Group updated successfully!"})

@group_blueprint.route('/group/<int:id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    if not group:
        return jsonify({"message": "Group not found!"}), 404

    db.session.delete(group)
    db.session.commit()
    return jsonify({"message": "Group deleted successfully!"})
