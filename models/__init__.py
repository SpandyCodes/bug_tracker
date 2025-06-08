from flask_sqlalchemy import SQLAlchemy
from models import db

# This file is used to make 'models' a package and expose 'db' to other modules
db = SQLAlchemy()
db.init_app(app)