from flask import Blueprint, request, jsonify
from models.resource import Resource
from database import db

resource_blueprint = Blueprint('resource', __name__)

@resource_blueprint.route('/resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    new_resource = Resource(name=data['name'], role=data['role'], region=data['region'],
                            hourly_rate=data['hourly_rate'], total_time=data['total_time'],
                            forecasted_cost=data['forecasted_cost'], monthly_hours=data['monthly_hours'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added successfully!"}), 201

@resource_blueprint.route('/resource', methods=['GET'])
def get_all_resources():
    resources = Resource.query.all()
    output = []
    for resource in resources:
        resource_data = {"id": resource.id, "name": resource.name, "role": resource.role, 
                         "region": resource.region, "hourly_rate": resource.hourly_rate,
                         "total_time": resource.total_time, "forecasted_cost": resource.forecasted_cost,
                         "monthly_hours": resource.monthly_hours}
        output.append(resource_data)
    return jsonify({"resources": output})

@resource_blueprint.route('/resource/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found!"}), 404

    data = request.get_json()
    resource.name = data['name']
    resource.role = data['role']
    resource.region = data['region']
    resource.hourly_rate = data['hourly_rate']
    resource.total_time = data['total_time']
    resource.forecasted_cost = data['forecasted_cost']
    resource.monthly_hours = data['monthly_hours']
    db.session.commit()
    return jsonify({"message": "Resource updated successfully!"})

@resource_blueprint.route('/resource/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found!"}), 404

    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted successfully!"})

