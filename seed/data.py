import uuid


def uid() -> str:
    return str(uuid.uuid4())


# Corridor
CORRIDOR_THIKA_RD = uid()

# SACCOs
SACCO_UMOINER = uid()
SACCO_GITHURAI_45 = uid()
SACCO_GITHURAI_44 = uid()
SACCO_LUCKY_SUMMER = uid()
SACCO_KASARANI = uid()
SACCO_MIREMA = uid()
SACCO_TRM = uid()   # Thika Road Mall shuttle (panya)
SACCO_CLAY_CITY = uid()   # Clay City panya

# Stages (formal)
STAGE_CBD_GPO = uid()   # General Post Office / Archives roundabout
STAGE_MFANGANO = uid()   # Mfangano St stage (outbound city side)
STAGE_PANGANI = uid()
STAGE_MUTHAIGA = uid()
STAGE_KASARANI_STAGE = uid()
STAGE_MIREMA_STAGE = uid()
STAGE_TRM_STAGE = uid()   # Thika Road Mall
STAGE_GITHURAI_45 = uid()
STAGE_GITHURAI_44 = uid()
STAGE_LUCKY_SUMMER = uid()
STAGE_CLAY_CITY = uid()   # panya terminus
STAGE_UMOINER_TERMINUS = uid()   # Umoja / Outering Rd junction (informal terminus)
STAGE_ROOFTOPS = uid()   # informal panya stage off Eastern bypass
STAGE_FISHPONDS = uid()   # informal / semi-formal
STAGE_GARDEN_ESTATE = uid()

# Public holiday IDs
PH_NEW_YEAR = uid()
PH_GOOD_FRIDAY = uid()
PH_EASTER_MON = uid()
PH_LABOUR_DAY = uid()
PH_MADARAKA = uid()
PH_MASHUJAA = uid()
PH_JAMHURI = uid()
PH_CHRISTMAS = uid()
PH_BOXING = uid()


CORRIDORS = [
    {
        "id":          CORRIDOR_THIKA_RD,
        "name":        "Thika Road",
        "description": "A8 highway corridor from CBD to Thika town. "
                       "Includes formal routes, panya (shortcut) routes via "
                       "Mirema, Lucky Summer, Clay City and the Eastern bypass.",
        "is_active":   True,
    }
]

SACCOS = [
    {
        "id": SACCO_UMOINER, "name": "Umoiner Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Githurai 45 / Outering Road",
        "operating_status": "active", "safety_rating": 3.2,
        "comfort_rating": 2.9, "is_verified": True,
    },
    {
        "id": SACCO_GITHURAI_45, "name": "Githurai 45 Matatu Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Githurai 45",
        "operating_status": "active", "safety_rating": 3.0,
        "comfort_rating": 2.8, "is_verified": True,
    },
    {
        "id": SACCO_GITHURAI_44, "name": "Githurai 44 Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Githurai 44",
        "operating_status": "active", "safety_rating": 3.1,
        "comfort_rating": 2.7, "is_verified": True,
    },
    {
        "id": SACCO_LUCKY_SUMMER, "name": "Lucky Summer Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Lucky Summer",
        "operating_status": "active", "safety_rating": 3.4,
        "comfort_rating": 3.0, "is_verified": True,
    },
    {
        "id": SACCO_KASARANI, "name": "Kasarani Express Sacco",
        "vehicle_type": "32-seater", "is_electric": False,
        "terminus_area": "Kasarani Stadium",
        "operating_status": "active", "safety_rating": 3.6,
        "comfort_rating": 3.3, "is_verified": True,
    },
    {
        "id": SACCO_MIREMA, "name": "Mirema Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Mirema Drive",
        "operating_status": "active", "safety_rating": 3.2,
        "comfort_rating": 3.0, "is_verified": False,
    },
    {
        "id": SACCO_TRM, "name": "TRM Shuttle Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Thika Road Mall",
        "operating_status": "active", "safety_rating": 3.5,
        "comfort_rating": 3.2, "is_verified": False,
    },
    {
        "id": SACCO_CLAY_CITY, "name": "Clay City Panya Sacco",
        "vehicle_type": "14-seater", "is_electric": False,
        "terminus_area": "Clay City / Eastern Bypass",
        "operating_status": "active", "safety_rating": 2.9,
        "comfort_rating": 2.6, "is_verified": False,
    },
]

SACCO_ALIASES = [
    {"id": uid(), "sacco_id": SACCO_UMOINER,
     "alias": "Umoiner",      "alias_type": "colloquial"},
    {"id": uid(), "sacco_id": SACCO_GITHURAI_45,  "alias": "45",
     "alias_type": "abbreviation"},
    {"id": uid(), "sacco_id": SACCO_GITHURAI_45,
     "alias": "Githurai",     "alias_type": "colloquial"},
    {"id": uid(), "sacco_id": SACCO_GITHURAI_44,  "alias": "44",
     "alias_type": "abbreviation"},
    {"id": uid(), "sacco_id": SACCO_LUCKY_SUMMER,
     "alias": "Lucky",        "alias_type": "colloquial"},
    {"id": uid(), "sacco_id": SACCO_KASARANI,
     "alias": "Kasarani",     "alias_type": "colloquial"},
    {"id": uid(), "sacco_id": SACCO_MIREMA,
     "alias": "Mirema Drive", "alias_type": "colloquial"},
    {"id": uid(), "sacco_id": SACCO_TRM,          "alias": "TRM",
     "alias_type": "abbreviation"},
    {"id": uid(), "sacco_id": SACCO_CLAY_CITY,
     "alias": "Clay",         "alias_type": "colloquial"},
]

STAGES = [
    {
        "id": STAGE_CBD_GPO, "name": "GPO / Archives Roundabout",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "General Post Office, Archives building",
        "landmark_sw": "Posta Kuu, jengo la Archives",
        "latitude": -1.283200, "longitude": 36.821500, "is_active": True,
    },
    {
        "id": STAGE_MFANGANO, "name": "Mfangano Street Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Mfangano St opposite Machakos Bus Station end",
        "landmark_sw": "Mtaa wa Mfangano",
        "latitude": -1.284900, "longitude": 36.822800, "is_active": True,
    },
    {
        "id": STAGE_PANGANI, "name": "Pangani Stage",
        "area": "Pangani", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Pangani Girls High School junction",
        "landmark_sw": "Makutano ya Pangani Girls",
        "latitude": -1.269100, "longitude": 36.836700, "is_active": True,
    },
    {
        "id": STAGE_MUTHAIGA, "name": "Muthaiga Mini Market",
        "area": "Muthaiga", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Muthaiga Mini Market / Total petrol station",
        "landmark_sw": "Muthaiga Mini Market",
        "latitude": -1.254300, "longitude": 36.842100, "is_active": True,
    },
    {
        "id": STAGE_KASARANI_STAGE, "name": "Kasarani Stadium Stage",
        "area": "Kasarani", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Safaricom Stadium Kasarani (main gate)",
        "landmark_sw": "Uwanja wa Kasarani",
        "latitude": -1.222300, "longitude": 36.893400, "is_active": True,
    },
    {
        "id": STAGE_TRM_STAGE, "name": "Thika Road Mall Stage",
        "area": "Roysambu", "stage_type": "formal", "direction": "outbound",
        "landmark":    "TRM – main gate bus bay",
        "landmark_sw": "Lango kuu la TRM",
        "latitude": -1.209800, "longitude": 36.889600, "is_active": True,
    },
    {
        "id": STAGE_GITHURAI_45, "name": "Githurai 45 Stage",
        "area": "Githurai", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Githurai 45 terminus near Equity Bank",
        "landmark_sw": "Mwisho wa Githurai 45",
        "latitude": -1.175400, "longitude": 36.923100, "is_active": True,
    },
    {
        "id": STAGE_GITHURAI_44, "name": "Githurai 44 Stage",
        "area": "Githurai", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Githurai 44 junction – Outering Road",
        "landmark_sw": "Makutano ya Githurai 44 na Outering Road",
        "latitude": -1.184600, "longitude": 36.913800, "is_active": True,
    },
    {
        "id": STAGE_LUCKY_SUMMER, "name": "Lucky Summer Drop-off",
        "area": "Lucky Summer", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Lucky Summer estate entrance, near Shell station",
        "landmark_sw": "Ingilio la Lucky Summer",
        "latitude": -1.242600, "longitude": 36.870900, "is_active": True,
    },
    {
        "id": STAGE_MIREMA_STAGE, "name": "Mirema Drive Stage",
        "area": "Mirema", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Mirema Drive opposite Mirema Springs estate",
        "landmark_sw": "Mirema Drive karibu na Mirema Springs",
        "latitude": -1.232800, "longitude": 36.876500, "is_active": True,
    },
    {
        "id": STAGE_CLAY_CITY, "name": "Clay City Panya Terminus",
        "area": "Clay City", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Clay City estate gate off Eastern Bypass",
        "landmark_sw": "Lango la Clay City",
        "latitude": -1.196200, "longitude": 36.904100, "is_active": True,
    },
    {
        "id": STAGE_ROOFTOPS, "name": "Rooftops / Bypass Stage",
        "area": "Rooftops", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Rooftops estate junction, Eastern Bypass",
        "landmark_sw": "Makutano ya Rooftops na Eastern Bypass",
        "latitude": -1.199000, "longitude": 36.899300, "is_active": True,
    },
    {
        "id": STAGE_FISHPONDS, "name": "Fish Ponds Stage",
        "area": "Fishponds", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Fish Ponds / Garden Square area",
        "landmark_sw": "Eneo la Fish Ponds",
        "latitude": -1.215300, "longitude": 36.888700, "is_active": True,
    },
    {
        "id": STAGE_GARDEN_ESTATE, "name": "Garden Estate Stage",
        "area": "Garden Estate", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Garden Estate Road junction off Thika Rd",
        "landmark_sw": "Makutano ya Garden Estate na Thika Road",
        "latitude": -1.237400, "longitude": 36.862000, "is_active": True,
    },
    {
        "id": STAGE_UMOINER_TERMINUS, "name": "Umoiner / Outering Terminus",
        "area": "Githurai", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Outering Road / Githurai 45 Umoiner base",
        "landmark_sw": "Kituo cha Umoiner Outering",
        "latitude": -1.178300, "longitude": 36.918500, "is_active": True,
    },
]

STAGE_HOURS = []
# All main stages: Mon–Fri 05:00–22:30, Sat 05:30–22:00, Sun/PH 06:00–21:00
MAIN_STAGE_IDS = [
    STAGE_CBD_GPO, STAGE_MFANGANO, STAGE_PANGANI, STAGE_MUTHAIGA,
    STAGE_KASARANI_STAGE, STAGE_TRM_STAGE, STAGE_GITHURAI_45, STAGE_GITHURAI_44,
]
PANYA_STAGE_IDS = [
    STAGE_LUCKY_SUMMER, STAGE_MIREMA_STAGE, STAGE_CLAY_CITY,
    STAGE_ROOFTOPS, STAGE_FISHPONDS, STAGE_GARDEN_ESTATE, STAGE_UMOINER_TERMINUS,
]
_HOURS = {
    # day_of_week (0=Mon … 6=Sun): (open_from, open_until)
    0: ("05:00", "22:30"), 1: ("05:00", "22:30"), 2: ("05:00", "22:30"),
    3: ("05:00", "22:30"), 4: ("05:00", "23:00"), 5: ("05:30", "22:00"),
    6: ("06:00", "21:00"),
}
_PANYA_HOURS = {
    0: ("06:00", "21:00"), 1: ("06:00", "21:00"), 2: ("06:00", "21:00"),
    3: ("06:00", "21:00"), 4: ("06:00", "22:00"), 5: ("06:30", "21:00"),
    6: ("07:00", "19:00"),
}
for sid in MAIN_STAGE_IDS:
    for dow, (ofrom, ountil) in _HOURS.items():
        STAGE_HOURS.append({"id": uid(), "stage_id": sid, "day_of_week": dow,
                            "open_from": ofrom, "open_until": ountil})
for sid in PANYA_STAGE_IDS:
    for dow, (ofrom, ountil) in _PANYA_HOURS.items():
        STAGE_HOURS.append({"id": uid(), "stage_id": sid, "day_of_week": dow,
                            "open_from": ofrom, "open_until": ountil})

ROUTE_45_OUT = uid()
ROUTE_45_IN = uid()
ROUTE_44_OUT = uid()
ROUTE_44_IN = uid()
ROUTE_LUCKY_OUT = uid()
ROUTE_LUCKY_IN = uid()
ROUTE_KAS_OUT = uid()
ROUTE_KAS_IN = uid()
ROUTE_MIREMA_OUT = uid()
ROUTE_MIREMA_IN = uid()
ROUTE_TRM_OUT = uid()
ROUTE_TRM_IN = uid()
ROUTE_CLAY_OUT = uid()
ROUTE_CLAY_IN = uid()
ROUTE_UMOINER_OUT = uid()
ROUTE_UMOINER_IN = uid()

ROUTES = [
    {
        "id": ROUTE_45_OUT, "sacco_id": SACCO_GITHURAI_45,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_GITHURAI_45,
        "via_description": "via Pangani, Muthaiga, Kasarani, TRM",
        "via_description_sw": "kupitia Pangani, Muthaiga, Kasarani, TRM",
        "distance_km": 18.4, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 8, "avg_duration_mins": 55,
        "peak_duration_mins": 90,
    },
    {
        "id": ROUTE_45_IN, "sacco_id": SACCO_GITHURAI_45,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_GITHURAI_45, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via TRM, Kasarani, Muthaiga, Pangani",
        "via_description_sw": "kupitia TRM, Kasarani, Muthaiga, Pangani",
        "distance_km": 18.4, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 8, "avg_duration_mins": 50,
        "peak_duration_mins": 85,
    },
    {
        "id": ROUTE_44_OUT, "sacco_id": SACCO_GITHURAI_44,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_GITHURAI_44,
        "via_description": "via Pangani, Muthaiga, Kasarani",
        "via_description_sw": "kupitia Pangani, Muthaiga, Kasarani",
        "distance_km": 16.8, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 10, "avg_duration_mins": 50,
        "peak_duration_mins": 80,
    },
    {
        "id": ROUTE_44_IN, "sacco_id": SACCO_GITHURAI_44,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_GITHURAI_44, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Kasarani, Muthaiga, Pangani",
        "via_description_sw": "kupitia Kasarani, Muthaiga, Pangani",
        "distance_km": 16.8, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 10, "avg_duration_mins": 45,
        "peak_duration_mins": 75,
    },
    {
        "id": ROUTE_LUCKY_OUT, "sacco_id": SACCO_LUCKY_SUMMER,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_LUCKY_SUMMER,
        "via_description": "via Pangani, Garden Estate, Lucky Summer (panya)",
        "via_description_sw": "kupitia Pangani, Garden Estate (panya)",
        "distance_km": 11.2, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 30,
        "peak_duration_mins": 50,
    },
    {
        "id": ROUTE_LUCKY_IN, "sacco_id": SACCO_LUCKY_SUMMER,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_LUCKY_SUMMER, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Garden Estate, Pangani (panya shortcut)",
        "via_description_sw": "kupitia Garden Estate, Pangani (panya)",
        "distance_km": 11.2, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 28,
        "peak_duration_mins": 45,
    },
    {
        "id": ROUTE_KAS_OUT, "sacco_id": SACCO_KASARANI,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_KASARANI_STAGE,
        "via_description": "via Pangani, Muthaiga (express – limited stops)",
        "via_description_sw": "kupitia Pangani, Muthaiga (express)",
        "distance_km": 12.6, "is_express": True,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 30,
        "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_KAS_IN, "sacco_id": SACCO_KASARANI,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_KASARANI_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Muthaiga, Pangani (express – limited stops)",
        "via_description_sw": "kupitia Muthaiga, Pangani (express)",
        "distance_km": 12.6, "is_express": True,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 28,
        "peak_duration_mins": 50,
    },
    {
        "id": ROUTE_MIREMA_OUT, "sacco_id": SACCO_MIREMA,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_MIREMA_STAGE,
        "via_description": "via Pangani, Mirema Drive (panya off Thika Rd)",
        "via_description_sw": "kupitia Pangani, Mirema Drive (panya)",
        "distance_km": 12.9, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 35,
        "peak_duration_mins": 60,
    },
    {
        "id": ROUTE_MIREMA_IN, "sacco_id": SACCO_MIREMA,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MIREMA_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Mirema Drive, Pangani (panya)",
        "via_description_sw": "kupitia Mirema Drive, Pangani (panya)",
        "distance_km": 12.9, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 33,
        "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_TRM_OUT, "sacco_id": SACCO_TRM,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_TRM_STAGE,
        "via_description": "via Pangani, Muthaiga, Fish Ponds",
        "via_description_sw": "kupitia Pangani, Muthaiga, Fish Ponds",
        "distance_km": 14.7, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 40,
        "peak_duration_mins": 70,
    },
    {
        "id": ROUTE_TRM_IN, "sacco_id": SACCO_TRM,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_TRM_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Fish Ponds, Muthaiga, Pangani",
        "via_description_sw": "kupitia Fish Ponds, Muthaiga, Pangani",
        "distance_km": 14.7, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 38,
        "peak_duration_mins": 65,
    },
    {
        "id": ROUTE_CLAY_OUT, "sacco_id": SACCO_CLAY_CITY,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_CLAY_CITY,
        "via_description": "via Rooftops, Eastern Bypass (panya)",
        "via_description_sw": "kupitia Rooftops, Eastern Bypass (panya)",
        "distance_km": 13.5, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 35,
        "peak_duration_mins": 60,
    },
    {
        "id": ROUTE_CLAY_IN, "sacco_id": SACCO_CLAY_CITY,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CLAY_CITY, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Eastern Bypass, Rooftops (panya)",
        "via_description_sw": "kupitia Eastern Bypass, Rooftops (panya)",
        "distance_km": 13.5, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 33,
        "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_UMOINER_OUT, "sacco_id": SACCO_UMOINER,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MFANGANO, "dest_stage_id": STAGE_UMOINER_TERMINUS,
        "via_description": "via Pangani, Githurai 45 (Outering branch)",
        "via_description_sw": "kupitia Pangani, Githurai 45 (tawi la Outering)",
        "distance_km": 19.1, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 58,
        "peak_duration_mins": 95,
    },
    {
        "id": ROUTE_UMOINER_IN, "sacco_id": SACCO_UMOINER,
        "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_UMOINER_TERMINUS, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "via Githurai 45, Pangani (Outering branch)",
        "via_description_sw": "kupitia Githurai 45, Pangani (tawi la Outering)",
        "distance_km": 19.1, "is_express": False,
        "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 52,
        "peak_duration_mins": 88,
    },
]

ROUTE_PATHS = [
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_MFANGANO,       "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_PANGANI,         "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_GARDEN_ESTATE,   "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_MUTHAIGA,        "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_FISHPONDS,       "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_TRM_STAGE,       "stop_order": 6},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_KASARANI_STAGE,  "stop_order": 7},
    {"id": uid(), "route_id": ROUTE_45_OUT,
     "stage_id": STAGE_GITHURAI_45,     "stop_order": 8},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_GITHURAI_45,      "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_KASARANI_STAGE,   "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_TRM_STAGE,        "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_FISHPONDS,        "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_MUTHAIGA,         "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_GARDEN_ESTATE,    "stop_order": 6},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_PANGANI,          "stop_order": 7},
    {"id": uid(), "route_id": ROUTE_45_IN,
     "stage_id": STAGE_CBD_GPO,          "stop_order": 8},
    {"id": uid(), "route_id": ROUTE_LUCKY_OUT,
     "stage_id": STAGE_MFANGANO,     "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_LUCKY_OUT,
     "stage_id": STAGE_PANGANI,      "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_LUCKY_OUT,
     "stage_id": STAGE_GARDEN_ESTATE, "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_LUCKY_OUT,
     "stage_id": STAGE_LUCKY_SUMMER, "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_LUCKY_IN,
     "stage_id": STAGE_LUCKY_SUMMER,  "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_LUCKY_IN,
     "stage_id": STAGE_GARDEN_ESTATE, "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_LUCKY_IN,
     "stage_id": STAGE_PANGANI,       "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_LUCKY_IN,
     "stage_id": STAGE_CBD_GPO,       "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_KAS_OUT,
     "stage_id": STAGE_MFANGANO,       "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_KAS_OUT,
     "stage_id": STAGE_PANGANI,        "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_KAS_OUT,
     "stage_id": STAGE_MUTHAIGA,       "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_KAS_OUT,
     "stage_id": STAGE_KASARANI_STAGE, "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_KAS_IN,
     "stage_id": STAGE_KASARANI_STAGE,  "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_KAS_IN,
     "stage_id": STAGE_MUTHAIGA,        "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_KAS_IN,
     "stage_id": STAGE_PANGANI,         "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_KAS_IN,
     "stage_id": STAGE_CBD_GPO,         "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_MIREMA_OUT,
     "stage_id": STAGE_MFANGANO,    "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_MIREMA_OUT,
     "stage_id": STAGE_PANGANI,     "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_MIREMA_OUT,
     "stage_id": STAGE_LUCKY_SUMMER, "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_MIREMA_OUT,
     "stage_id": STAGE_MIREMA_STAGE, "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_MIREMA_IN,
     "stage_id": STAGE_MIREMA_STAGE, "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_MIREMA_IN,
     "stage_id": STAGE_LUCKY_SUMMER, "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_MIREMA_IN,
     "stage_id": STAGE_PANGANI,      "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_MIREMA_IN,
     "stage_id": STAGE_CBD_GPO,      "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_TRM_OUT,
     "stage_id": STAGE_MFANGANO,       "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_TRM_OUT,
     "stage_id": STAGE_PANGANI,        "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_TRM_OUT,
     "stage_id": STAGE_MUTHAIGA,       "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_TRM_OUT,
     "stage_id": STAGE_FISHPONDS,      "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_TRM_OUT,
     "stage_id": STAGE_TRM_STAGE,      "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_TRM_IN,
     "stage_id": STAGE_TRM_STAGE,       "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_TRM_IN,
     "stage_id": STAGE_FISHPONDS,       "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_TRM_IN,
     "stage_id": STAGE_MUTHAIGA,        "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_TRM_IN,
     "stage_id": STAGE_PANGANI,         "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_TRM_IN,
     "stage_id": STAGE_CBD_GPO,         "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_CLAY_OUT,
     "stage_id": STAGE_MFANGANO,      "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_CLAY_OUT,
     "stage_id": STAGE_ROOFTOPS,      "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_CLAY_OUT,
     "stage_id": STAGE_CLAY_CITY,     "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_CLAY_IN,
     "stage_id": STAGE_CLAY_CITY,      "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_CLAY_IN,
     "stage_id": STAGE_ROOFTOPS,       "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_CLAY_IN,
     "stage_id": STAGE_CBD_GPO,        "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_MFANGANO,       "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_PANGANI,        "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_MUTHAIGA,       "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_KASARANI_STAGE, "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_GITHURAI_45,    "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_UMOINER_OUT,
     "stage_id": STAGE_UMOINER_TERMINUS, "stop_order": 6},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_UMOINER_TERMINUS, "stop_order": 1},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_GITHURAI_45,     "stop_order": 2},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_KASARANI_STAGE,  "stop_order": 3},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_MUTHAIGA,        "stop_order": 4},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_PANGANI,         "stop_order": 5},
    {"id": uid(), "route_id": ROUTE_UMOINER_IN,
     "stage_id": STAGE_CBD_GPO,         "stop_order": 6},
]

# fare_type, day_type (0=weekday,5=Sat,6=Sun), amount, valid_from, valid_until
_FARE_DEFS = [
    # (route_out, route_in, peak_kes, offpeak_kes, late_kes, weekend_kes)
    (ROUTE_45_OUT,     ROUTE_45_IN,     70,  60,  80,  65),
    (ROUTE_44_OUT,     ROUTE_44_IN,     60,  50,  70,  55),
    (ROUTE_LUCKY_OUT,  ROUTE_LUCKY_IN,  50,  40,  60,  45),
    (ROUTE_KAS_OUT,    ROUTE_KAS_IN,    60,  50,  70,  55),
    (ROUTE_MIREMA_OUT, ROUTE_MIREMA_IN, 55,  45,  65,  50),
    (ROUTE_TRM_OUT,    ROUTE_TRM_IN,    65,  55,  75,  60),
    (ROUTE_CLAY_OUT,   ROUTE_CLAY_IN,   55,  45,  65,  50),
    (ROUTE_UMOINER_OUT, ROUTE_UMOINER_IN, 70,  60,  80,  65),
]

FARES = []
for (rout, rin, peak, offpeak, late, wkend) in _FARE_DEFS:
    for route_id in (rout, rin):
        FARES += [
            {"id": uid(), "route_id": route_id, "fare_type": "peak",
             "day_type": 0, "amount_kes": peak,    "valid_from": "06:00", "valid_until": "09:00"},
            {"id": uid(), "route_id": route_id, "fare_type": "peak",
             "day_type": 0, "amount_kes": peak,    "valid_from": "16:30", "valid_until": "19:30"},
            {"id": uid(), "route_id": route_id, "fare_type": "off_peak",
             "day_type": 0, "amount_kes": offpeak, "valid_from": "09:00", "valid_until": "16:30"},
            {"id": uid(), "route_id": route_id, "fare_type": "late_night",
             "day_type": 0, "amount_kes": late,    "valid_from": "21:00", "valid_until": "23:59"},
            {"id": uid(), "route_id": route_id, "fare_type": "weekend",
             "day_type": 5, "amount_kes": wkend,   "valid_from": "00:00", "valid_until": "23:59"},
            {"id": uid(), "route_id": route_id, "fare_type": "weekend",
             "day_type": 6, "amount_kes": wkend,   "valid_from": "00:00", "valid_until": "23:59"},
        ]

PAYMENT_METHODS = []
ALL_ROUTE_IDS = [r["id"] for r in ROUTES]
for rid in ALL_ROUTE_IDS:
    PAYMENT_METHODS.append({"id": uid(), "route_id": rid, "method": "cash"})
    PAYMENT_METHODS.append({"id": uid(), "route_id": rid, "method": "mpesa"})

PUBLIC_HOLIDAYS = [
    {"id": PH_NEW_YEAR,   "name": "New Year's Day",
        "holiday_date": "2026-01-01", "is_recurring": True,  "year": None},
    {"id": PH_GOOD_FRIDAY, "name": "Good Friday",
        "holiday_date": "2026-04-03", "is_recurring": False, "year": 2026},
    {"id": PH_EASTER_MON, "name": "Easter Monday",
        "holiday_date": "2026-04-06", "is_recurring": False, "year": 2026},
    {"id": PH_LABOUR_DAY, "name": "Labour Day",
        "holiday_date": "2026-05-01", "is_recurring": True,  "year": None},
    {"id": PH_MADARAKA,   "name": "Madaraka Day",
        "holiday_date": "2026-06-01", "is_recurring": True,  "year": None},
    {"id": PH_MASHUJAA,   "name": "Mashujaa Day",
        "holiday_date": "2026-10-20", "is_recurring": True,  "year": None},
    {"id": PH_JAMHURI,    "name": "Jamhuri Day",
        "holiday_date": "2026-12-12", "is_recurring": True,  "year": None},
    {"id": PH_CHRISTMAS,  "name": "Christmas Day",
        "holiday_date": "2026-12-25", "is_recurring": True,  "year": None},
    {"id": PH_BOXING,     "name": "Boxing Day",
        "holiday_date": "2026-12-26", "is_recurring": True,  "year": None},
]

# hour_slot = 0-23; sample_count seeded with realistic estimate
OCCUPANCY = []
_OCC_PROFILE = {
    # hour: (weekday_load, sat_load, sun_load)
    5:  (0.35, 0.20, 0.15),
    6:  (0.70, 0.40, 0.25),
    7:  (0.95, 0.55, 0.30),
    8:  (0.98, 0.60, 0.35),
    9:  (0.75, 0.65, 0.40),
    10: (0.55, 0.70, 0.50),
    11: (0.45, 0.72, 0.55),
    12: (0.50, 0.75, 0.60),
    13: (0.55, 0.70, 0.58),
    14: (0.50, 0.65, 0.55),
    15: (0.55, 0.60, 0.50),
    16: (0.80, 0.65, 0.45),
    17: (0.98, 0.70, 0.50),
    18: (0.97, 0.68, 0.48),
    19: (0.80, 0.60, 0.42),
    20: (0.55, 0.50, 0.35),
    21: (0.35, 0.38, 0.28),
    22: (0.20, 0.25, 0.18),
}
for rid in ALL_ROUTE_IDS:
    for hour, (wd, sat, sun) in _OCC_PROFILE.items():
        # weekdays (0–4)
        for dow in range(5):
            OCCUPANCY.append({"id": uid(), "route_id": rid, "day_of_week": dow,
                              "hour_slot": hour, "avg_load_factor": wd, "sample_count": 120})
        OCCUPANCY.append({"id": uid(), "route_id": rid, "day_of_week": 5,
                          "hour_slot": hour, "avg_load_factor": sat, "sample_count": 60})
        OCCUPANCY.append({"id": uid(), "route_id": rid, "day_of_week": 6,
                          "hour_slot": hour, "avg_load_factor": sun, "sample_count": 40})

APP_SETTINGS = [
    {"key": "corridor_surge_enabled", "value": "true",
     "description": "Toggle corridor surge pricing globally"},
    {"key": "late_night_threshold_hour", "value": "21",
     "description": "Hour (24h) after which late_night fare applies"},
    {"key": "transfer_search_max_legs", "value": "2",
     "description": "Maximum transfer legs in route search"},
    {"key": "default_currency", "value": "KES",
     "description": "ISO 4217 currency code"},
    {"key": "fare_correction_review_days", "value": "7",
     "description": "Days before unreviewed fare corrections auto-expire"},
]
