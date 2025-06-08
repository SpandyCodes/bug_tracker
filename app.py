from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize core Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = app.config['LOGIN_VIEW']

# Import models to register with SQLAlchemy metadata
from models import user, bug

# Import and register Blueprints (route handlers)
from routes.auth import auth_blueprint
from routes.bug_api import bug_blueprint

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(bug_blueprint, url_prefix="/api")

# Simple health check route
@app.route("/")
def index():
    return "<h3>🚀 Bug Tracker is running with Flask + OOP + Vercel ready!</h3>"

# Local dev entry point
if __name__ == "__main__":
    app.run(debug=True)