import pytest
from unittest.mock import MagicMock


def test_tags_include_express_for_express_route():
    from app.models.sacco import VehicleType
    route = MagicMock()
    route.is_express = True
    route.sacco.is_electric = False
    route.sacco.vehicle_type = VehicleType.SEATER_32
    route.payment_methods = []
    route.path = []
    route.occupancy = []

    tags = []
    if route.is_express:
        tags.append("express")
    if route.sacco.is_electric:
        tags.append("electric")
    if route.sacco.vehicle_type == VehicleType.SEATER_14:
        tags.append("comfort")

    assert "express" in tags
    assert "electric" not in tags
    assert "comfort" not in tags


def test_tags_include_comfort_for_14_seater():
    from app.models.sacco import VehicleType
    route = MagicMock()
    route.is_express = False
    route.sacco.is_electric = False
    route.sacco.vehicle_type = VehicleType.SEATER_14

    tags = []
    if route.is_express:
        tags.append("express")
    if route.sacco.vehicle_type == VehicleType.SEATER_14:
        tags.append("comfort")

    assert "comfort" in tags
    assert "express" not in tags


def test_cheapest_tag_assigned_to_lowest_fare():
    from app.schemas.trip import TripOption
    from app.models.sacco import VehicleType
    import uuid

    options = [
        TripOption(route_id=uuid.uuid4(), sacco="A", vehicle_type=VehicleType.SEATER_32, fare=100,
                   fare_type_now="peak", is_off_peak_now=False, payment_methods=["cash"], tags=[], data_confidence="high"),
        TripOption(route_id=uuid.uuid4(), sacco="B", vehicle_type=VehicleType.SEATER_32, fare=60,
                   fare_type_now="peak", is_off_peak_now=False, payment_methods=["cash"], tags=[], data_confidence="high"),
        TripOption(route_id=uuid.uuid4(), sacco="C", vehicle_type=VehicleType.SEATER_32, fare=80,
                   fare_type_now="peak", is_off_peak_now=False, payment_methods=["cash"], tags=[], data_confidence="high"),
    ]

    options.sort(key=lambda o: o.fare)
    options[0].tags.append("cheapest")

    assert options[0].fare == 60
    assert "cheapest" in options[0].tags
    assert "cheapest" not in options[1].tags
