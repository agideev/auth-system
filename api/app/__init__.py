# Flask: creates the application and allows returning JSON responses.
from flask import Flask, jsonify
from flask_cors import CORS

# Flask-Migrate: manages database migrations.
from flask_migrate import Migrate

# JWTManager: configures the JWT authentication system.
from flask_jwt_extended import JWTManager

# Application settings, including database and JWT.
from config import Config

# SQLAlchemy instance used by the application.
from .extensions import db

# Imports the models so SQLAlchemy knows about their tables.
from .models import User

# Blueprint responsible for authentication routes.
from .routes.auth_routes import auth_bp



def create_app():
    # Creates the main Flask application instance.
    app = Flask(__name__)


    # Loads the settings defined in the Config class.
    app.config.from_object(Config)

    # Initializes SQLAlchemy with the application.
    db.init_app(app)

    # Configures Flask-Migrate to manage database migrations.
    Migrate(app, db)

    # Initializes the JWT authentication system.
    JWTManager(app)

    # Registers the authentication routes in the application.
    app.register_blueprint(auth_bp)

    CORS(app)


    @app.get("/health")
    def health():
        try:
            # Tests if the application can execute a query in the database.
            db.session.execute(db.text("SELECT 1"))

            return jsonify({
                "success": True,
                "message": "API and database are running"
            })

        except Exception as error:
            # Returns an error if the database connection fails.
            return jsonify({
                "success": False,
                "message": "Database connection failed",
                "error": str(error)
            }), 500

    # Returns the configured Flask application.
    return app
