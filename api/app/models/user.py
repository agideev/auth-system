# Used to store the user's creation and update date and time.
from datetime import datetime, timezone

from app.extensions import db


# Model that represents the "users" table in the database.
class User(db.Model):
    __tablename__ = "users"

    # Unique user identifier.
    id = db.Column(db.Integer, primary_key=True)

    # Username. Cannot be empty and must be unique.
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # User email. Cannot be empty and must be unique.
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    # Stores the password securely using a hash.
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Indicates whether the user account is active.
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # Date and time when the user was created.
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Date and time of the user's last update.
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
