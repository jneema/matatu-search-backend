import pytest


@pytest.mark.asyncio
async def test_correction_submit_nonexistent_route_returns_404(client):
    # The nil UUID does not correspond to any route in the DB.
    # The endpoint should reject it with 404 rather than 500.
    response = await client.post(
        "/api/v1/routes/00000000-0000-0000-0000-000000000000/fare-correction",
        json={"reported_amount_kes": 100, "fare_type": "peak"}
    )
    assert response.status_code == 404
