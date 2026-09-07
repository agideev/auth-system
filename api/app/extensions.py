# Flask-Migrate: manages database migrations.
from flask_migrate import Migrate

# Flask-SQLAlchemy: integrates SQLAlchemy with Flask.
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance used to work with the database.
db = SQLAlchemy()

# Flask-Migrate instance used to manage migrations.
migrate = Migrate()
