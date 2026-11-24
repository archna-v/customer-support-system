
import os
import uuid

# Use a separate MongoDB database for testing
os.environ["MONGO_DATABASE"] = "customer_support_test_db"

from fastapi.testclient import TestClient

from app.main import app
from app.auth.auth_service import hash_password
from app.database.mongodb import users_collection


client = TestClient(app)


# Helper function to create test users with specific roles
def create_test_user(username, password, role):

    users_collection.insert_one({
        "username": username,
        "password": hash_password(password),
        "role": role
    })


# 1. Test root endpoint
def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Customer Support System API is running"
    )


# 2. Test customer registration
def test_register_user():
    username = f"pytest_user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200
    assert "user_id" in response.json()


# 3. Test customer login
def test_login_user():
    username = f"pytest_login_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"


# 4. Test authenticated customer can get tickets
def test_authenticated_user_can_get_tickets():
    username = f"pytest_customer_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


# 5. Test customer cannot update tickets
def test_customer_cannot_update_ticket():
    username = f"pytest_customer_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    ticket_response = client.post(
        "/tickets",
        json={
            "title": "RBAC Automated Test",
            "description": "Testing customer permissions.",
            "priority": "Medium"
        },
        headers=headers
    )

    assert ticket_response.status_code == 200

    ticket_id = ticket_response.json()["ticket_id"]

    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": "Critical"
        },
        headers=headers
    )

    assert update_response.status_code == 403


# 6. Test Support Agent permissions
def test_support_agent_permissions():
    username = f"pytest_agent_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Create Support Agent directly in test database
    create_test_user(username, password, "Support Agent")

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    ticket_response = client.post(
        "/tickets",
        json={
            "title": "Support Agent RBAC Test",
            "description": "Testing support agent permissions.",
            "priority": "Medium"
        },
        headers=headers
    )

    assert ticket_response.status_code == 200

    ticket_id = ticket_response.json()["ticket_id"]

    # Support Agent CAN update
    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": "High"
        },
        headers=headers
    )

    assert update_response.status_code == 200

    # Support Agent CANNOT delete
    delete_response = client.delete(
        f"/tickets/{ticket_id}",
        headers=headers
    )

    assert delete_response.status_code == 403


# 7. Test Admin permissions
def test_admin_can_delete_ticket():
    username = f"pytest_admin_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Create Admin directly in test database
    create_test_user(username, password, "Admin")

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    ticket_response = client.post(
        "/tickets",
        json={
            "title": "Admin RBAC Test",
            "description": "Testing admin permissions.",
            "priority": "Medium"
        },
        headers=headers
    )

    assert ticket_response.status_code == 200

    ticket_id = ticket_response.json()["ticket_id"]

    # Admin CAN update
    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": "Critical"
        },
        headers=headers
    )

    assert update_response.status_code == 200

    # Admin CAN delete
    delete_response = client.delete(
        f"/tickets/{ticket_id}",
        headers=headers
    )

    assert delete_response.status_code == 200
