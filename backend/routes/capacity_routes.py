from flask import Blueprint, request, jsonify
import calendar
import holidays
from models.resource import Resource
from models.pto_holidays import PTOHoliday
from models.release_schedule import ReleaseSchedule
from database import db


capacity_blueprint = Blueprint('capacity', __name__)

def working_days(year, month, region):
    weekdays_in_month = calendar.monthcalendar(year, month)
    
    # Fetch the holidays based on the region
    if region == 'US':
        country_holidays = holidays.UnitedStates(years=year)
    elif region == 'India':
        country_holidays = holidays.India(years=year)
    elif region == 'Argentina':
        country_holidays = holidays.Argentina(years=year)
    elif region == 'Spain':
        country_holidays = holidays.Spain(years=year)
    else:
        country_holidays = {}
    
    # Counting the number of weekdays (assuming Saturday and Sunday are non-working days)
    # and subtracting holidays
    return sum(1 for week in weekdays_in_month for day in week[0:5] if day != 0 and f"{year}-{month:02d}-{day:02d}" not in country_holidays)

@capacity_blueprint.route('/capacity/<int:resource_id>/<int:year>/<int:month>', methods=['GET'])
def get_capacity(resource_id, year, month):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found!"}), 404
    
    base_hours = working_days(year, month, resource.region) * 8

    # Subtract PTO (this is a simplified example and might need adjustments)
    pto_hours = sum(pto.hours for pto in PTOHoliday.query.filter_by(resource_id=resource_id, date__year=year, date__month=month))

    available_hours = base_hours - pto_hours

    return jsonify({"resource_id": resource_id, "year": year, "month": month, "available_hours": available_hours})

@capacity_blueprint.route('/role_capacity/<role>/<int:year>/<int:month>', methods=['GET'])
def get_role_capacity(role, year, month):
    # Fetch all resources with the specified role
    resources = Resource.query.filter_by(role=role).all()
    if not resources:
        return jsonify({"message": f"No resources found for role {role}!"}), 404

    total_available_hours = 0

    # Calculate the start and end of the month
    start_of_month = f"{year}-{month}-01"
    end_of_month = f"{year}-{month}-{calendar.monthrange(year, month)[1]}"
    
    # Check for release schedules overlapping with the month and role
    overlapping_releases = ReleaseSchedule.query.filter(
        ReleaseSchedule.role == role,
        ReleaseSchedule.start_date <= end_of_month,
        ReleaseSchedule.end_date >= start_of_month
    ).all()

    release_hours_per_resource = sum(release.hours for release in overlapping_releases) / len(resources)

    # Calculate capacity for each resource and add to the total
    for resource in resources:
        base_hours = working_days(year, month, resource.region) * 8
        pto_hours = sum(pto.hours for pto in PTOHoliday.query.filter_by(resource_id=resource.id, date__year=year, date__month=month))
        total_available_hours += (base_hours - pto_hours - release_hours_per_resource)

    return jsonify({"role": role, "year": year, "month": month, "available_hours": total_available_hours})


