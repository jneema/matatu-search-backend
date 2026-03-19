import pytest


@pytest.mark.asyncio
async def test_bundle_unknown_corridor(client):
    response = await client.get("/api/v1/bundle/00000000-0000-0000-0000-000000000000")
    assert response.status_code in (200, 404)
