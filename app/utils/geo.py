from geopy.distance import geodesic


def distance_meters(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return geodesic((lat1, lng1), (lat2, lng2)).meters


def is_within_radius(
    user_lat: float,
    user_lng: float,
    stage_lat: float,
    stage_lng: float,
    radius_m: float = 300.0,
) -> bool:
    return distance_meters(user_lat, user_lng, stage_lat, stage_lng) <= radius_m