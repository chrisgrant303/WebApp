from flask import Flask
from database import db
from routes.group_routes import group_blueprint
from routes.budget_routes import budget_blueprint
from routes.pto_holidays_routes import pto_holidays_blueprint
from routes.release_schedule_routes import release_schedule_blueprint
from routes.capacity_routes import capacity_blueprint
from routes.resource_routes import resource_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registering blueprints
app.register_blueprint(group_blueprint)
app.register_blueprint(budget_blueprint)
app.register_blueprint(pto_holidays_blueprint)
app.register_blueprint(release_schedule_blueprint)
app.register_blueprint(capacity_blueprint)
app.register_blueprint(resource_blueprint)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)