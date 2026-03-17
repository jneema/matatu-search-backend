def trip_search_key(origin_id: str, dest_id: str, hour: int) -> str:
    return f"trip_search:{origin_id}:{dest_id}:{hour}"


def corridor_bundle_key(corridor_id: str) -> str:
    return f"corridor_bundle:{corridor_id}"


def active_surges_key(corridor_id: str) -> str:
    return f"active_surges:{corridor_id}"


def stage_list_key(area: str) -> str:
    return f"stage_list:{area.lower()}"