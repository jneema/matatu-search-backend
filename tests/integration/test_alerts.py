import pytest


@pytest.mark.asyncio
async def test_list_alerts_returns_200(client):
    response = await client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_surges_returns_200(client):
    response = await client.get("/api/v1/alerts/surges")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
