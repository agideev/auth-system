import uuid

from app import create_app
from app.services.auth_service import create_user


# Default password used in tests.
PASSWORD = "Senha123456"


def create_test_user():
    # Generates unique data to avoid conflicts in the database.
    username = f"test_{uuid.uuid4().hex}_pytest_user"
    email = f"test_{uuid.uuid4().hex}@example.com"

    return username, email


def get_access_token(client, email, password):
    # Logs in to get the JWT used in protected routes.
    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    data = response.get_json()

    # Confirms that the login was successful.
    assert response.status_code == 200
    assert data["success"] is True

    return data["access_token"]


def test_register_route():
    app = create_app()

    username, email = create_test_user()

    client = app.test_client()

    # Sends data to register a new user.
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": PASSWORD
        }
    )

    data = response.get_json()

    # Verifies if the user was registered correctly.
    assert response.status_code == 201
    assert data["success"] is True
    assert data["message"] == "User registered successfully."
    assert data["user"]["username"] == username
    assert data["user"]["email"] == email
    assert data["access_token"] is not None


def test_login_route():
    app = create_app()

    username, email = create_test_user()

    # Creates the user before testing login.
    with app.app_context():
        create_user(
            username=username,
            email=email,
            password=PASSWORD
        )

    client = app.test_client()

    # Logs in to verify if the API generates a JWT.
    access_token = get_access_token(
        client,
        email,
        PASSWORD
    )

    assert access_token is not None


def test_me_route():
    app = create_app()

    username, email = create_test_user()

    # Creates the user to be queried.
    with app.app_context():
        create_user(
            username=username,
            email=email,
            password=PASSWORD
        )

    client = app.test_client()

    # Gets the JWT needed to access the protected route.
    access_token = get_access_token(
        client,
        email,
        PASSWORD
    )

    # Queries the authenticated user's data.
    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    data = response.get_json()

    # Verifies if the API returned the correct data.
    assert response.status_code == 200
    assert data["success"] is True
    assert data["user"]["username"] == username
    assert data["user"]["email"] == email
    assert data["user"]["is_active"] is True


def test_update_profile_route():
    app = create_app()

    username, email = create_test_user()

    # Creates the user whose profile will be updated.
    with app.app_context():
        create_user(
            username=username,
            email=email,
            password=PASSWORD
        )

    client = app.test_client()

    # Gets the JWT needed to update the profile.
    access_token = get_access_token(
        client,
        email,
        PASSWORD
    )

    # Generates new unique data for the profile.
    new_username = f"updated_{uuid.uuid4().hex}"
    new_email = f"updated_{uuid.uuid4().hex}@example.com"

    # Sends the new data to the API.
    response = client.put(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "username": new_username,
            "email": new_email
        }
    )

    data = response.get_json()

    # Verifies if the profile was updated correctly.
    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Profile updated successfully."
    assert data["user"]["username"] == new_username
    assert data["user"]["email"] == new_email


def test_update_password_route():
    app = create_app()

    username, email = create_test_user()

    # Defines a new password to test the update.
    new_password = "NovaSenha123456"

    # Creates the user with the current password.
    with app.app_context():
        create_user(
            username=username,
            email=email,
            password=PASSWORD
        )

    client = app.test_client()

    # Gets the JWT needed to change the password.
    access_token = get_access_token(
        client,
        email,
        PASSWORD
    )

    # Sends the current password and the new password to the API.
    response = client.put(
        "/api/auth/me/password",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "current_password": PASSWORD,
            "new_password": new_password
        }
    )

    data = response.get_json()

    # Verifies if the password was updated correctly.
    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Password updated successfully."
