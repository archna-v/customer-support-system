import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Customer Support System API is running"
    )


def test_register_user():
    username = f"pytest_user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "Test@12345",
            "role": "Customer"
        }
    )

    assert response.status_code == 200
    assert "user_id" in response.json()


def test_login_user():
    username = f"pytest_login_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Register user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "role": "Customer"
        }
    )

    assert register_response.status_code == 200

    # Login
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


def test_authenticated_user_can_get_tickets():
    username = f"pytest_customer_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Register customer
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "role": "Customer"
        }
    )

    assert register_response.status_code == 200

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/tickets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_customer_cannot_update_ticket():
    username = f"pytest_customer_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Register customer
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "role": "Customer"
        }
    )

    assert register_response.status_code == 200

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Create ticket
    ticket_response = client.post(
        "/tickets",
        json={
            "title": "RBAC Automated Test",
            "description": "Testing customer permissions.",
            "priority": "Medium"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert ticket_response.status_code == 200

    ticket_id = ticket_response.json()["ticket_id"]

    # Try to update ticket
    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={
            "priority": "Critical"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert update_response.status_code == 403

def test_support_agent_permissions():
    username = f"pytest_agent_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Register Support Agent
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "role": "Support Agent"
        }
    )

    assert register_response.status_code == 200

    # Login
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

    # Create ticket
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

def test_admin_can_delete_ticket():
    username = f"pytest_admin_{uuid.uuid4().hex[:8]}"
    password = "Test@12345"

    # Register Admin
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
            "role": "Admin"
        }
    )

    assert register_response.status_code == 200

    # Login
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

    # Create ticket
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