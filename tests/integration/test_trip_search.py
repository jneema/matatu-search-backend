import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_trip_search_returns_200(client):
    response = await client.get("/api/v1/trips/search?origin=Juja&destination=CBD")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert "all_options" in data
    assert data["trip"] != ""


@pytest.mark.asyncio
async def test_trip_search_unknown_origin_returns_404(client):
    response = await client.get("/api/v1/trips/search?origin=Xyznonexistent&destination=CBD")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_trip_search_scenarios_structure(client):
    response = await client.get("/api/v1/trips/search?origin=Juja&destination=CBD")
    data = response.json()
    scenarios = data["scenarios"]
    assert "express" in scenarios
    assert "cheapest" in scenarios
    assert "comfort" in scenarios
    assert "electric" in scenarios
    assert "off_peak" in scenarios


@pytest.mark.asyncio
async def test_admin_requires_auth(client):
    response = await client.get("/api/v1/admin/corrections/pending")
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_admin_login_and_access(client):
    login = await client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "matatu-admin-2024"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/admin/corrections/pending",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
