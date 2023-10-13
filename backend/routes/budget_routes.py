from flask import Blueprint, request, jsonify
from models.budget import Budget
from database import db

budget_blueprint = Blueprint('budget', __name__)

@budget_blueprint.route('/budget', methods=['POST'])
def add_budget():
    data = request.get_json()
    new_budget = Budget(initial_budget=data['initial_budget'], adjustments=data['adjustments'])
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({"message": "Budget added successfully!"}), 201

@budget_blueprint.route('/budget', methods=['GET'])
def get_all_budgets():
    budgets = Budget.query.all()
    output = [{"id": budget.id, "initial_budget": budget.initial_budget, "adjustments": budget.adjustments} for budget in budgets]
    return jsonify({"budgets": output})

@budget_blueprint.route('/budget/<int:id>', methods=['PUT'])
def update_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({"message": "Budget entry not found!"}), 404

    data = request.get_json()
    budget.initial_budget = data['initial_budget']
    budget.adjustments = data['adjustments']
    db.session.commit()
    return jsonify({"message": "Budget updated successfully!"})

@budget_blueprint.route('/budget/<int:id>', methods=['DELETE'])
def delete_budget(id):
    budget = Budget.query.get(id)
    if not budget:
        return jsonify({"message": "Budget entry not found!"}), 404

    db.session.delete(budget)
    db.session.commit()
    return jsonify({"message": "Budget deleted successfully!"})
