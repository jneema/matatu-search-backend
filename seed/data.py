CORRIDOR_THIKA_RD = "a1000000-0000-0000-0000-000000000001"

CORRIDORS = [
    {
        "id":          CORRIDOR_THIKA_RD,
        "name":        "Thika Road",
        "description": (
            "A8 highway corridor from Nairobi CBD to Thika town (~42 km). "
            "Includes formal trunk routes, panya (shortcut) routes via Mirema, "
            "Lucky Summer, Clay City and the Eastern Bypass, and long-distance "
            "routes continuing to Ruiru, Juja and Thika."
        ),
        "is_active": True,
    }
]

SACCO_UMOINER = "b1000000-0000-0000-0000-000000000001"
SACCO_GITHURAI_45 = "b1000000-0000-0000-0000-000000000002"
SACCO_GITHURAI_44 = "b1000000-0000-0000-0000-000000000003"
SACCO_LUCKY_SUMMER = "b1000000-0000-0000-0000-000000000004"
SACCO_KASARANI = "b1000000-0000-0000-0000-000000000005"
SACCO_MIREMA = "b1000000-0000-0000-0000-000000000006"
SACCO_TRM = "b1000000-0000-0000-0000-000000000007"
SACCO_CLAY_CITY = "b1000000-0000-0000-0000-000000000008"
SACCO_RUIRU = "b1000000-0000-0000-0000-000000000009"
SACCO_JUJA = "b1000000-0000-0000-0000-000000000010"
SACCO_THIKA = "b1000000-0000-0000-0000-000000000011"

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
    {
        "id": SACCO_RUIRU, "name": "Ruiru Matatu Sacco",
        "vehicle_type": "32-seater", "is_electric": False,
        "terminus_area": "Ruiru Town",
        "operating_status": "active", "safety_rating": 3.3,
        "comfort_rating": 3.0, "is_verified": True,
    },
    {
        "id": SACCO_JUJA, "name": "Juja / JKUAT Sacco",
        "vehicle_type": "52-seater", "is_electric": False,
        "terminus_area": "Juja Town / JKUAT Gate",
        "operating_status": "active", "safety_rating": 3.4,
        "comfort_rating": 3.1, "is_verified": True,
    },
    {
        "id": SACCO_THIKA, "name": "Thika Shuttle Sacco",
        "vehicle_type": "52-seater", "is_electric": False,
        "terminus_area": "Thika Town Bus Park",
        "operating_status": "active", "safety_rating": 3.5,
        "comfort_rating": 3.2, "is_verified": True,
    },
]

SACCO_ALIASES = [
    {"id": "c1000000-0000-0000-0000-000000000001", "sacco_id": SACCO_UMOINER,
        "alias": "Umoiner",      "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000002", "sacco_id": SACCO_GITHURAI_45,
        "alias": "45",           "alias_type": "abbreviation"},
    {"id": "c1000000-0000-0000-0000-000000000003", "sacco_id": SACCO_GITHURAI_45,
        "alias": "Githurai",     "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000004", "sacco_id": SACCO_GITHURAI_44,
        "alias": "44",           "alias_type": "abbreviation"},
    {"id": "c1000000-0000-0000-0000-000000000005", "sacco_id": SACCO_LUCKY_SUMMER,
        "alias": "Lucky",        "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000006", "sacco_id": SACCO_KASARANI,
        "alias": "Kasarani",     "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000007", "sacco_id": SACCO_MIREMA,
        "alias": "Mirema Drive", "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000008", "sacco_id": SACCO_TRM,
        "alias": "TRM",          "alias_type": "abbreviation"},
    {"id": "c1000000-0000-0000-0000-000000000009", "sacco_id": SACCO_CLAY_CITY,
        "alias": "Clay",         "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000010", "sacco_id": SACCO_RUIRU,
        "alias": "Ruiru",        "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000011", "sacco_id": SACCO_JUJA,
        "alias": "Juja",         "alias_type": "colloquial"},
    {"id": "c1000000-0000-0000-0000-000000000012", "sacco_id": SACCO_JUJA,
        "alias": "JKUAT",        "alias_type": "abbreviation"},
    {"id": "c1000000-0000-0000-0000-000000000013", "sacco_id": SACCO_THIKA,
        "alias": "Thika",        "alias_type": "colloquial"},
]


# inbound terminus (GPO/Archives)
STAGE_CBD_GPO = "d1000000-0000-0000-0000-000000000001"
# Githurai 45 outbound (OTC/Latema)
STAGE_CBD_OTC = "d1000000-0000-0000-0000-000000000002"
# Githurai 44 / Umoiner outbound
STAGE_CBD_KOJA = "d1000000-0000-0000-0000-000000000003"
# Kasarani Express outbound
STAGE_CBD_AMBASSADOR = "d1000000-0000-0000-0000-000000000004"
# Ruiru / Juja / Thika outbound
STAGE_CBD_KENCOM = "d1000000-0000-0000-0000-000000000005"
STAGE_CBD_RAILWAYS = "d1000000-0000-0000-0000-000000000006"  # TRM / Clay City outbound
# Lucky Summer / Mirema outbound
STAGE_CBD_AFYA = "d1000000-0000-0000-0000-000000000007"

STAGE_PANGANI = "d1000000-0000-0000-0000-000000000008"
STAGE_MUTHAIGA = "d1000000-0000-0000-0000-000000000009"
STAGE_GARDEN_ESTATE = "d1000000-0000-0000-0000-000000000010"
STAGE_LUCKY_SUMMER = "d1000000-0000-0000-0000-000000000011"
STAGE_MIREMA_STAGE = "d1000000-0000-0000-0000-000000000012"
STAGE_FISHPONDS = "d1000000-0000-0000-0000-000000000013"

STAGE_KASARANI_STAGE = "d1000000-0000-0000-0000-000000000014"
STAGE_TRM_STAGE = "d1000000-0000-0000-0000-000000000015"
STAGE_ROOFTOPS = "d1000000-0000-0000-0000-000000000016"
STAGE_CLAY_CITY = "d1000000-0000-0000-0000-000000000017"

STAGE_GITHURAI_45 = "d1000000-0000-0000-0000-000000000018"
STAGE_GITHURAI_44 = "d1000000-0000-0000-0000-000000000019"
STAGE_UMOINER_TERMINUS = "d1000000-0000-0000-0000-000000000020"

STAGE_KAHAWA_SUKARI = "d1000000-0000-0000-0000-000000000021"
STAGE_KAHAWA_WEST = "d1000000-0000-0000-0000-000000000022"
STAGE_RUIRU_STAGE = "d1000000-0000-0000-0000-000000000023"
STAGE_KIMBO = "d1000000-0000-0000-0000-000000000024"
STAGE_JUJA_STAGE = "d1000000-0000-0000-0000-000000000025"
STAGE_JUJA_FARM = "d1000000-0000-0000-0000-000000000026"
STAGE_THIKA_STAGE = "d1000000-0000-0000-0000-000000000027"

STAGES = [
    {
        "id": STAGE_CBD_GPO, "name": "GPO / Archives Roundabout",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "General Post Office, Archives building",
        "landmark_sw": "Posta Kuu, jengo la Archives",
        "latitude": -1.283200, "longitude": 36.821500, "is_active": True,
    },
    {
        "id": STAGE_CBD_OTC, "name": "OTC Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Odeon Cinema / OTC, Latema Road",
        "landmark_sw": "Sinema ya Odeon, Latema Road",
        "latitude": -1.284200, "longitude": 36.822100, "is_active": True,
    },
    {
        "id": STAGE_CBD_KOJA, "name": "Koja Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Koja bus terminus, River Road",
        "landmark_sw": "Stendi ya Koja, River Road",
        "latitude": -1.282800, "longitude": 36.822900, "is_active": True,
    },
    {
        "id": STAGE_CBD_AMBASSADOR, "name": "Ambassador / Moi Avenue Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Ambassador Hotel, Moi Avenue",
        "landmark_sw": "Hoteli ya Ambassador, Moi Avenue",
        "latitude": -1.284600, "longitude": 36.820300, "is_active": True,
    },
    {
        "id": STAGE_CBD_KENCOM, "name": "Kencom Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Kencom House, Moi Avenue",
        "landmark_sw": "Kencom House, Moi Avenue",
        "latitude": -1.285100, "longitude": 36.820800, "is_active": True,
    },
    {
        "id": STAGE_CBD_RAILWAYS, "name": "Railways / Haile Selassie Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Nairobi Railway Station, Haile Selassie Avenue",
        "landmark_sw": "Stesheni ya Reli, Haile Selassie Avenue",
        "latitude": -1.287800, "longitude": 36.821400, "is_active": True,
    },
    {
        "id": STAGE_CBD_AFYA, "name": "Afya Centre Stage",
        "area": "Nairobi CBD", "stage_type": "formal", "direction": "inbound",
        "landmark":    "Afya Centre building, Tubman Road",
        "landmark_sw": "Jengo la Afya Centre, Tubman Road",
        "latitude": -1.283600, "longitude": 36.823700, "is_active": True,
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
        "id": STAGE_GARDEN_ESTATE, "name": "Garden Estate Stage",
        "area": "Garden Estate", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Garden Estate Road junction off Thika Road",
        "landmark_sw": "Makutano ya Garden Estate na Thika Road",
        "latitude": -1.237400, "longitude": 36.862000, "is_active": True,
    },
    {
        "id": STAGE_LUCKY_SUMMER, "name": "Lucky Summer Stage",
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
        "id": STAGE_FISHPONDS, "name": "Fish Ponds Stage",
        "area": "Fishponds", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Fish Ponds / Garden Square area",
        "landmark_sw": "Eneo la Fish Ponds",
        "latitude": -1.215300, "longitude": 36.888700, "is_active": True,
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
        "id": STAGE_ROOFTOPS, "name": "Rooftops / Bypass Stage",
        "area": "Rooftops", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Rooftops estate junction, Eastern Bypass",
        "landmark_sw": "Makutano ya Rooftops na Eastern Bypass",
        "latitude": -1.199000, "longitude": 36.899300, "is_active": True,
    },
    {
        "id": STAGE_CLAY_CITY, "name": "Clay City Panya Terminus",
        "area": "Clay City", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Clay City estate gate off Eastern Bypass",
        "landmark_sw": "Lango la Clay City",
        "latitude": -1.196200, "longitude": 36.904100, "is_active": True,
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
        "id": STAGE_UMOINER_TERMINUS, "name": "Umoiner / Outering Terminus",
        "area": "Githurai", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Outering Road / Githurai 45 Umoiner base",
        "landmark_sw": "Kituo cha Umoiner Outering",
        "latitude": -1.178300, "longitude": 36.918500, "is_active": True,
    },

    {
        "id": STAGE_KAHAWA_SUKARI, "name": "Kahawa Sukari Stage",
        "area": "Kahawa Sukari", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Kahawa Sukari estate gate, Thika Road",
        "landmark_sw": "Lango la Kahawa Sukari",
        "latitude": -1.186500, "longitude": 36.929200, "is_active": True,
    },
    {
        "id": STAGE_KAHAWA_WEST, "name": "Kahawa West Stage",
        "area": "Kahawa West", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Kahawa West junction, near KU Main campus",
        "landmark_sw": "Makutano ya Kahawa West, karibu na KU",
        "latitude": -1.181200, "longitude": 36.935800, "is_active": True,
    },
    {
        "id": STAGE_RUIRU_STAGE, "name": "Ruiru Town Stage",
        "area": "Ruiru", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Ruiru town centre, Thika Road / Kamiti Road junction",
        "landmark_sw": "Katikati ya Ruiru",
        "latitude": -1.145800, "longitude": 36.961700, "is_active": True,
    },
    {
        "id": STAGE_KIMBO, "name": "Kimbo Stage",
        "area": "Kimbo", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Kimbo area, Thika Road between Ruiru and Juja",
        "landmark_sw": "Eneo la Kimbo",
        "latitude": -1.117300, "longitude": 36.990200, "is_active": True,
    },
    {
        "id": STAGE_JUJA_STAGE, "name": "Juja Town Stage",
        "area": "Juja", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Juja town centre / JKUAT main gate junction",
        "landmark_sw": "Katikati ya Juja / Lango kuu la JKUAT",
        "latitude": -1.103600, "longitude": 37.014200, "is_active": True,
    },
    {
        "id": STAGE_JUJA_FARM, "name": "Juja Farm Stage",
        "area": "Juja Farm", "stage_type": "informal", "direction": "outbound",
        "landmark":    "Juja Farm area, past JKUAT gate",
        "landmark_sw": "Eneo la Juja Farm",
        "latitude": -1.094100, "longitude": 37.025500, "is_active": True,
    },
    {
        "id": STAGE_THIKA_STAGE, "name": "Thika Town Bus Park",
        "area": "Thika", "stage_type": "formal", "direction": "outbound",
        "landmark":    "Thika town main bus park, off Kenyatta Highway",
        "landmark_sw": "Stendi kuu ya Thika",
        "latitude": -1.033200, "longitude": 37.069400, "is_active": True,
    },
]


STAGE_ALIASES = [
    {"id": "e1000000-0000-0000-0000-000000000001", "stage_id": STAGE_CBD_GPO,
        "alias": "CBD",             "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000002", "stage_id": STAGE_CBD_GPO,
        "alias": "Town",            "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000003", "stage_id": STAGE_CBD_GPO,
        "alias": "Nairobi",         "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000004", "stage_id": STAGE_CBD_GPO,
        "alias": "GPO",             "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000005", "stage_id": STAGE_CBD_OTC,
        "alias": "OTC",             "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000006", "stage_id": STAGE_CBD_OTC,
        "alias": "Odeon",           "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000007", "stage_id": STAGE_CBD_OTC,
        "alias": "Latema",          "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000008", "stage_id": STAGE_CBD_KOJA,
        "alias": "Koja",            "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000009", "stage_id": STAGE_CBD_KOJA,
        "alias": "River Road",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000010", "stage_id": STAGE_CBD_AMBASSADOR,
        "alias": "Ambassador",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000011", "stage_id": STAGE_CBD_AMBASSADOR,
        "alias": "Moi Avenue",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000012", "stage_id": STAGE_CBD_KENCOM,
        "alias": "Kencom",          "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000013", "stage_id": STAGE_CBD_RAILWAYS,
        "alias": "Railways",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000014", "stage_id": STAGE_CBD_RAILWAYS,
        "alias": "Haile Selassie",  "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000015", "stage_id": STAGE_CBD_AFYA,
        "alias": "Afya Centre",     "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000016", "stage_id": STAGE_CBD_AFYA,
        "alias": "Afya",            "alias_type": "colloquial"},

    {"id": "e1000000-0000-0000-0000-000000000017", "stage_id": STAGE_PANGANI,
        "alias": "Pangani",         "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000018", "stage_id": STAGE_MUTHAIGA,
        "alias": "Muthaiga",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000019", "stage_id": STAGE_GARDEN_ESTATE,
        "alias": "Garden",          "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000020", "stage_id": STAGE_GARDEN_ESTATE,
        "alias": "Garden Estate",   "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000021", "stage_id": STAGE_LUCKY_SUMMER,
        "alias": "Lucky",           "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000022", "stage_id": STAGE_LUCKY_SUMMER,
        "alias": "Lucky Summer",    "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000023", "stage_id": STAGE_MIREMA_STAGE,
        "alias": "Mirema",          "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000024", "stage_id": STAGE_FISHPONDS,
        "alias": "Fish Ponds",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000025", "stage_id": STAGE_FISHPONDS,
        "alias": "Fishponds",       "alias_type": "colloquial"},

    {"id": "e1000000-0000-0000-0000-000000000026", "stage_id": STAGE_KASARANI_STAGE,
        "alias": "Kasarani",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000027", "stage_id": STAGE_KASARANI_STAGE,
        "alias": "Stadium",         "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000028", "stage_id": STAGE_TRM_STAGE,
        "alias": "TRM",             "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000029", "stage_id": STAGE_TRM_STAGE,
        "alias": "Thika Road Mall", "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000030", "stage_id": STAGE_TRM_STAGE,
        "alias": "Roysambu",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000031", "stage_id": STAGE_ROOFTOPS,
        "alias": "Rooftops",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000032", "stage_id": STAGE_CLAY_CITY,
        "alias": "Clay City",       "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000033", "stage_id": STAGE_CLAY_CITY,
        "alias": "Clay",            "alias_type": "colloquial"},

    {"id": "e1000000-0000-0000-0000-000000000034", "stage_id": STAGE_GITHURAI_45,
        "alias": "Githurai 45",     "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000035", "stage_id": STAGE_GITHURAI_45,
        "alias": "45",              "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000036", "stage_id": STAGE_GITHURAI_45,
        "alias": "Githurai",        "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000037", "stage_id": STAGE_GITHURAI_44,
        "alias": "Githurai 44",     "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000038", "stage_id": STAGE_GITHURAI_44,
        "alias": "44",              "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000039", "stage_id": STAGE_UMOINER_TERMINUS,
        "alias": "Umoiner",       "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000040", "stage_id": STAGE_UMOINER_TERMINUS,
        "alias": "Outering",      "alias_type": "colloquial"},

    {"id": "e1000000-0000-0000-0000-000000000041", "stage_id": STAGE_KAHAWA_SUKARI,
        "alias": "Kahawa Sukari",   "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000042", "stage_id": STAGE_KAHAWA_SUKARI,
        "alias": "Kahawa",          "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000043", "stage_id": STAGE_KAHAWA_WEST,
        "alias": "Kahawa West",     "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000044", "stage_id": STAGE_KAHAWA_WEST,
        "alias": "KU",              "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000045", "stage_id": STAGE_RUIRU_STAGE,
        "alias": "Ruiru",           "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000046", "stage_id": STAGE_RUIRU_STAGE,
        "alias": "Ruiru Town",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000047", "stage_id": STAGE_KIMBO,
        "alias": "Kimbo",           "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000048", "stage_id": STAGE_JUJA_STAGE,
        "alias": "Juja",            "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000049", "stage_id": STAGE_JUJA_STAGE,
        "alias": "JKUAT",           "alias_type": "abbreviation"},
    {"id": "e1000000-0000-0000-0000-000000000050", "stage_id": STAGE_JUJA_STAGE,
        "alias": "Juja Town",       "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000051", "stage_id": STAGE_JUJA_FARM,
        "alias": "Juja Farm",       "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000052", "stage_id": STAGE_THIKA_STAGE,
        "alias": "Thika",           "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000053", "stage_id": STAGE_THIKA_STAGE,
        "alias": "Thika Town",      "alias_type": "colloquial"},
    {"id": "e1000000-0000-0000-0000-000000000054", "stage_id": STAGE_THIKA_STAGE,
        "alias": "Thika Bus Park",  "alias_type": "colloquial"},
]

STAGE_HOURS = []

_MAIN_STAGE_IDS = [
    STAGE_CBD_GPO, STAGE_CBD_OTC, STAGE_CBD_KOJA,
    STAGE_CBD_AMBASSADOR, STAGE_CBD_KENCOM, STAGE_CBD_RAILWAYS, STAGE_CBD_AFYA,
    STAGE_PANGANI, STAGE_MUTHAIGA,
    STAGE_KASARANI_STAGE, STAGE_TRM_STAGE,
    STAGE_GITHURAI_45, STAGE_GITHURAI_44,
    STAGE_RUIRU_STAGE, STAGE_JUJA_STAGE, STAGE_THIKA_STAGE,
]
_PANYA_STAGE_IDS = [
    STAGE_GARDEN_ESTATE, STAGE_LUCKY_SUMMER, STAGE_MIREMA_STAGE,
    STAGE_FISHPONDS, STAGE_ROOFTOPS, STAGE_CLAY_CITY, STAGE_UMOINER_TERMINUS,
    STAGE_KAHAWA_SUKARI, STAGE_KAHAWA_WEST, STAGE_KIMBO, STAGE_JUJA_FARM,
]
_MAIN_HOURS = {0: ("05:00", "22:30"), 1: ("05:00", "22:30"), 2: ("05:00", "22:30"),
               3: ("05:00", "22:30"), 4: ("05:00", "23:00"), 5: ("05:30", "22:00"),
               6: ("06:00", "21:00")}
_PANYA_HOURS = {0: ("06:00", "21:00"), 1: ("06:00", "21:00"), 2: ("06:00", "21:00"),
                3: ("06:00", "21:00"), 4: ("06:00", "22:00"), 5: ("06:30", "21:00"),
                6: ("07:00", "19:00")}

# Stage-hours get sequential pinned IDs
_sh_counter = 1
for _sid in _MAIN_STAGE_IDS:
    for _dow, (_of, _ou) in _MAIN_HOURS.items():
        STAGE_HOURS.append({"id": f"f1000000-0000-0000-0000-{_sh_counter:012d}",
                            "stage_id": _sid, "day_of_week": _dow,
                            "open_from": _of, "open_until": _ou})
        _sh_counter += 1
for _sid in _PANYA_STAGE_IDS:
    for _dow, (_of, _ou) in _PANYA_HOURS.items():
        STAGE_HOURS.append({"id": f"f1000000-0000-0000-0000-{_sh_counter:012d}",
                            "stage_id": _sid, "day_of_week": _dow,
                            "open_from": _of, "open_until": _ou})
        _sh_counter += 1


ROUTE_45_OUT = "f2000000-0000-0000-0000-000000000001"
ROUTE_45_IN = "f2000000-0000-0000-0000-000000000002"
ROUTE_44_OUT = "f2000000-0000-0000-0000-000000000003"
ROUTE_44_IN = "f2000000-0000-0000-0000-000000000004"
ROUTE_LUCKY_OUT = "f2000000-0000-0000-0000-000000000005"
ROUTE_LUCKY_IN = "f2000000-0000-0000-0000-000000000006"
ROUTE_KAS_OUT = "f2000000-0000-0000-0000-000000000007"
ROUTE_KAS_IN = "f2000000-0000-0000-0000-000000000008"
ROUTE_MIREMA_OUT = "f2000000-0000-0000-0000-000000000009"
ROUTE_MIREMA_IN = "f2000000-0000-0000-0000-000000000010"
ROUTE_TRM_OUT = "f2000000-0000-0000-0000-000000000011"
ROUTE_TRM_IN = "f2000000-0000-0000-0000-000000000012"
ROUTE_CLAY_OUT = "f2000000-0000-0000-0000-000000000013"
ROUTE_CLAY_IN = "f2000000-0000-0000-0000-000000000014"
ROUTE_UMOINER_OUT = "f2000000-0000-0000-0000-000000000015"
ROUTE_UMOINER_IN = "f2000000-0000-0000-0000-000000000016"
ROUTE_RUIRU_OUT = "f2000000-0000-0000-0000-000000000017"
ROUTE_RUIRU_IN = "f2000000-0000-0000-0000-000000000018"
ROUTE_JUJA_OUT = "f2000000-0000-0000-0000-000000000019"
ROUTE_JUJA_IN = "f2000000-0000-0000-0000-000000000020"
ROUTE_THIKA_OUT = "f2000000-0000-0000-0000-000000000021"
ROUTE_THIKA_IN = "f2000000-0000-0000-0000-000000000022"

ROUTES = [
    {
        "id": ROUTE_45_OUT, "sacco_id": SACCO_GITHURAI_45, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_OTC, "dest_stage_id": STAGE_GITHURAI_45,
        "via_description": "OTC → Pangani → Muthaiga → Kasarani → TRM → Githurai 45",
        "via_description_sw": "OTC → Pangani → Muthaiga → Kasarani → TRM → Githurai 45",
        "distance_km": 18.4, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 8, "avg_duration_mins": 55, "peak_duration_mins": 90,
    },
    {
        "id": ROUTE_45_IN, "sacco_id": SACCO_GITHURAI_45, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_GITHURAI_45, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Githurai 45 → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Githurai 45 → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 18.4, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 8, "avg_duration_mins": 50, "peak_duration_mins": 85,
    },
    {
        "id": ROUTE_44_OUT, "sacco_id": SACCO_GITHURAI_44, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_KOJA, "dest_stage_id": STAGE_GITHURAI_44,
        "via_description": "Koja → Pangani → Muthaiga → Kasarani → Githurai 44",
        "via_description_sw": "Koja → Pangani → Muthaiga → Kasarani → Githurai 44",
        "distance_km": 16.8, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 10, "avg_duration_mins": 50, "peak_duration_mins": 80,
    },
    {
        "id": ROUTE_44_IN, "sacco_id": SACCO_GITHURAI_44, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_GITHURAI_44, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Githurai 44 → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Githurai 44 → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 16.8, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 10, "avg_duration_mins": 45, "peak_duration_mins": 75,
    },
    {
        "id": ROUTE_LUCKY_OUT, "sacco_id": SACCO_LUCKY_SUMMER, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_AFYA, "dest_stage_id": STAGE_LUCKY_SUMMER,
        "via_description": "Afya Centre → Pangani → Garden Estate → Lucky Summer (panya)",
        "via_description_sw": "Afya Centre → Pangani → Garden Estate → Lucky Summer (panya)",
        "distance_km": 11.2, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 30, "peak_duration_mins": 50,
    },
    {
        "id": ROUTE_LUCKY_IN, "sacco_id": SACCO_LUCKY_SUMMER, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_LUCKY_SUMMER, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Lucky Summer → Garden Estate → Pangani → GPO (panya)",
        "via_description_sw": "Lucky Summer → Garden Estate → Pangani → GPO (panya)",
        "distance_km": 11.2, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 28, "peak_duration_mins": 45,
    },
    {
        "id": ROUTE_KAS_OUT, "sacco_id": SACCO_KASARANI, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_AMBASSADOR, "dest_stage_id": STAGE_KASARANI_STAGE,
        "via_description": "Ambassador → Pangani → Muthaiga → Kasarani (express)",
        "via_description_sw": "Ambassador → Pangani → Muthaiga → Kasarani (express)",
        "distance_km": 12.6, "is_express": True, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 30, "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_KAS_IN, "sacco_id": SACCO_KASARANI, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_KASARANI_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Kasarani → Muthaiga → Pangani → GPO (express)",
        "via_description_sw": "Kasarani → Muthaiga → Pangani → GPO (express)",
        "distance_km": 12.6, "is_express": True, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 28, "peak_duration_mins": 50,
    },
    {
        "id": ROUTE_MIREMA_OUT, "sacco_id": SACCO_MIREMA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_AFYA, "dest_stage_id": STAGE_MIREMA_STAGE,
        "via_description": "Afya Centre → Pangani → Lucky Summer → Mirema Drive (panya)",
        "via_description_sw": "Afya Centre → Pangani → Lucky Summer → Mirema (panya)",
        "distance_km": 12.9, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 35, "peak_duration_mins": 60,
    },
    {
        "id": ROUTE_MIREMA_IN, "sacco_id": SACCO_MIREMA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_MIREMA_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Mirema Drive → Lucky Summer → Pangani → GPO (panya)",
        "via_description_sw": "Mirema → Lucky Summer → Pangani → GPO (panya)",
        "distance_km": 12.9, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 33, "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_TRM_OUT, "sacco_id": SACCO_TRM, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_RAILWAYS, "dest_stage_id": STAGE_TRM_STAGE,
        "via_description": "Railways → Pangani → Muthaiga → Fish Ponds → TRM",
        "via_description_sw": "Railways → Pangani → Muthaiga → Fish Ponds → TRM",
        "distance_km": 14.7, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 40, "peak_duration_mins": 70,
    },
    {
        "id": ROUTE_TRM_IN, "sacco_id": SACCO_TRM, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_TRM_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "TRM → Fish Ponds → Muthaiga → Pangani → GPO",
        "via_description_sw": "TRM → Fish Ponds → Muthaiga → Pangani → GPO",
        "distance_km": 14.7, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 12, "avg_duration_mins": 38, "peak_duration_mins": 65,
    },
    {
        "id": ROUTE_CLAY_OUT, "sacco_id": SACCO_CLAY_CITY, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_RAILWAYS, "dest_stage_id": STAGE_CLAY_CITY,
        "via_description": "Railways → Rooftops → Clay City (Eastern Bypass panya)",
        "via_description_sw": "Railways → Rooftops → Clay City (panya ya Eastern Bypass)",
        "distance_km": 13.5, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 35, "peak_duration_mins": 60,
    },
    {
        "id": ROUTE_CLAY_IN, "sacco_id": SACCO_CLAY_CITY, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CLAY_CITY, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Clay City → Rooftops → GPO (Eastern Bypass panya)",
        "via_description_sw": "Clay City → Rooftops → GPO (panya)",
        "distance_km": 13.5, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 33, "peak_duration_mins": 55,
    },
    {
        "id": ROUTE_UMOINER_OUT, "sacco_id": SACCO_UMOINER, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_KOJA, "dest_stage_id": STAGE_UMOINER_TERMINUS,
        "via_description": "Koja → Pangani → Muthaiga → Kasarani → Githurai 45 → Outering",
        "via_description_sw": "Koja → Pangani → Muthaiga → Kasarani → Githurai 45 → Outering",
        "distance_km": 19.1, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 58, "peak_duration_mins": 95,
    },
    {
        "id": ROUTE_UMOINER_IN, "sacco_id": SACCO_UMOINER, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_UMOINER_TERMINUS, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Outering → Githurai 45 → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Outering → Githurai 45 → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 19.1, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 15, "avg_duration_mins": 52, "peak_duration_mins": 88,
    },
    {
        "id": ROUTE_RUIRU_OUT, "sacco_id": SACCO_RUIRU, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_KENCOM, "dest_stage_id": STAGE_RUIRU_STAGE,
        "via_description": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Githurai 45 → Kahawa West → Ruiru",
        "via_description_sw": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Githurai 45 → Kahawa West → Ruiru",
        "distance_km": 28.6, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 75, "peak_duration_mins": 120,
    },
    {
        "id": ROUTE_RUIRU_IN, "sacco_id": SACCO_RUIRU, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_RUIRU_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Ruiru → Kahawa West → Githurai 45 → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Ruiru → Kahawa West → Githurai 45 → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 28.6, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 20, "avg_duration_mins": 70, "peak_duration_mins": 110,
    },
    {
        "id": ROUTE_JUJA_OUT, "sacco_id": SACCO_JUJA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_KENCOM, "dest_stage_id": STAGE_JUJA_STAGE,
        "via_description": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Kahawa Sukari → Ruiru → Kimbo → Juja",
        "via_description_sw": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Kahawa Sukari → Ruiru → Kimbo → Juja",
        "distance_km": 36.5, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 25, "avg_duration_mins": 90, "peak_duration_mins": 140,
    },
    {
        "id": ROUTE_JUJA_IN, "sacco_id": SACCO_JUJA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_JUJA_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Juja → Kimbo → Ruiru → Kahawa Sukari → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Juja → Kimbo → Ruiru → Kahawa Sukari → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 36.5, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 25, "avg_duration_mins": 85, "peak_duration_mins": 130,
    },
    {
        "id": ROUTE_THIKA_OUT, "sacco_id": SACCO_THIKA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_CBD_KENCOM, "dest_stage_id": STAGE_THIKA_STAGE,
        "via_description": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Ruiru → Juja → Thika",
        "via_description_sw": "Kencom → Pangani → Muthaiga → Kasarani → TRM → Ruiru → Juja → Thika",
        "distance_km": 42.3, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 30, "avg_duration_mins": 110, "peak_duration_mins": 160,
    },
    {
        "id": ROUTE_THIKA_IN, "sacco_id": SACCO_THIKA, "corridor_id": CORRIDOR_THIKA_RD,
        "origin_stage_id": STAGE_THIKA_STAGE, "dest_stage_id": STAGE_CBD_GPO,
        "via_description": "Thika → Juja → Ruiru → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "via_description_sw": "Thika → Juja → Ruiru → TRM → Kasarani → Muthaiga → Pangani → GPO",
        "distance_km": 42.3, "is_express": False, "route_status": "active",
        "departure_frequency_mins": 30, "avg_duration_mins": 105, "peak_duration_mins": 150,
    },
]


ROUTE_PATHS = []


def _stops(route_id, stage_ids):
    route_suffix = route_id[-12:] 
    
    return [
        {
            "id": f"a2{route_id[2:8]}-0000-0000-{i+1:04x}-{route_suffix}",
            "route_id": route_id,
            "stage_id": sid,
            "stop_order": i + 1
        }
        for i, sid in enumerate(stage_ids)
    ]

ROUTE_PATHS += _stops(ROUTE_45_OUT, [
    STAGE_CBD_OTC, STAGE_PANGANI, STAGE_GARDEN_ESTATE, STAGE_MUTHAIGA,
    STAGE_FISHPONDS, STAGE_TRM_STAGE, STAGE_KASARANI_STAGE, STAGE_GITHURAI_45,
])
ROUTE_PATHS += _stops(ROUTE_45_IN, [
    STAGE_GITHURAI_45, STAGE_KASARANI_STAGE, STAGE_TRM_STAGE, STAGE_FISHPONDS,
    STAGE_MUTHAIGA, STAGE_GARDEN_ESTATE, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_44_OUT, [
    STAGE_CBD_KOJA, STAGE_PANGANI, STAGE_MUTHAIGA,
    STAGE_KASARANI_STAGE, STAGE_GITHURAI_44,
])
ROUTE_PATHS += _stops(ROUTE_44_IN, [
    STAGE_GITHURAI_44, STAGE_KASARANI_STAGE, STAGE_MUTHAIGA,
    STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_LUCKY_OUT, [
    STAGE_CBD_AFYA, STAGE_PANGANI, STAGE_GARDEN_ESTATE, STAGE_LUCKY_SUMMER,
])
ROUTE_PATHS += _stops(ROUTE_LUCKY_IN, [
    STAGE_LUCKY_SUMMER, STAGE_GARDEN_ESTATE, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_KAS_OUT, [
    STAGE_CBD_AMBASSADOR, STAGE_PANGANI, STAGE_MUTHAIGA, STAGE_KASARANI_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_KAS_IN, [
    STAGE_KASARANI_STAGE, STAGE_MUTHAIGA, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_MIREMA_OUT, [
    STAGE_CBD_AFYA, STAGE_PANGANI, STAGE_LUCKY_SUMMER, STAGE_MIREMA_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_MIREMA_IN, [
    STAGE_MIREMA_STAGE, STAGE_LUCKY_SUMMER, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_TRM_OUT, [
    STAGE_CBD_RAILWAYS, STAGE_PANGANI, STAGE_MUTHAIGA,
    STAGE_FISHPONDS, STAGE_TRM_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_TRM_IN, [
    STAGE_TRM_STAGE, STAGE_FISHPONDS, STAGE_MUTHAIGA,
    STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_CLAY_OUT, [
    STAGE_CBD_RAILWAYS, STAGE_ROOFTOPS, STAGE_CLAY_CITY,
])
ROUTE_PATHS += _stops(ROUTE_CLAY_IN, [
    STAGE_CLAY_CITY, STAGE_ROOFTOPS, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_UMOINER_OUT, [
    STAGE_CBD_KOJA, STAGE_PANGANI, STAGE_MUTHAIGA, STAGE_KASARANI_STAGE,
    STAGE_GITHURAI_45, STAGE_UMOINER_TERMINUS,
])
ROUTE_PATHS += _stops(ROUTE_UMOINER_IN, [
    STAGE_UMOINER_TERMINUS, STAGE_GITHURAI_45, STAGE_KASARANI_STAGE,
    STAGE_MUTHAIGA, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_RUIRU_OUT, [
    STAGE_CBD_KENCOM, STAGE_PANGANI, STAGE_MUTHAIGA, STAGE_KASARANI_STAGE,
    STAGE_TRM_STAGE, STAGE_GITHURAI_45, STAGE_KAHAWA_SUKARI,
    STAGE_KAHAWA_WEST, STAGE_RUIRU_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_RUIRU_IN, [
    STAGE_RUIRU_STAGE, STAGE_KAHAWA_WEST, STAGE_KAHAWA_SUKARI,
    STAGE_GITHURAI_45, STAGE_TRM_STAGE, STAGE_KASARANI_STAGE,
    STAGE_MUTHAIGA, STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_JUJA_OUT, [
    STAGE_CBD_KENCOM, STAGE_PANGANI, STAGE_MUTHAIGA, STAGE_KASARANI_STAGE,
    STAGE_TRM_STAGE, STAGE_KAHAWA_SUKARI, STAGE_RUIRU_STAGE,
    STAGE_KIMBO, STAGE_JUJA_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_JUJA_IN, [
    STAGE_JUJA_STAGE, STAGE_KIMBO, STAGE_RUIRU_STAGE, STAGE_KAHAWA_SUKARI,
    STAGE_TRM_STAGE, STAGE_KASARANI_STAGE, STAGE_MUTHAIGA,
    STAGE_PANGANI, STAGE_CBD_GPO,
])
ROUTE_PATHS += _stops(ROUTE_THIKA_OUT, [
    STAGE_CBD_KENCOM, STAGE_PANGANI, STAGE_MUTHAIGA, STAGE_KASARANI_STAGE,
    STAGE_TRM_STAGE, STAGE_RUIRU_STAGE, STAGE_KIMBO,
    STAGE_JUJA_STAGE, STAGE_JUJA_FARM, STAGE_THIKA_STAGE,
])
ROUTE_PATHS += _stops(ROUTE_THIKA_IN, [
    STAGE_THIKA_STAGE, STAGE_JUJA_FARM, STAGE_JUJA_STAGE, STAGE_KIMBO,
    STAGE_RUIRU_STAGE, STAGE_TRM_STAGE, STAGE_KASARANI_STAGE,
    STAGE_MUTHAIGA, STAGE_PANGANI, STAGE_CBD_GPO,
])


_FARE_DEFS = [
    (ROUTE_45_OUT,      ROUTE_45_IN,       70,   60,   80,   65),
    (ROUTE_44_OUT,      ROUTE_44_IN,       60,   50,   70,   55),
    (ROUTE_LUCKY_OUT,   ROUTE_LUCKY_IN,    50,   40,   60,   45),
    (ROUTE_KAS_OUT,     ROUTE_KAS_IN,      60,   50,   70,   55),
    (ROUTE_MIREMA_OUT,  ROUTE_MIREMA_IN,   55,   45,   65,   50),
    (ROUTE_TRM_OUT,     ROUTE_TRM_IN,      65,   55,   75,   60),
    (ROUTE_CLAY_OUT,    ROUTE_CLAY_IN,     55,   45,   65,   50),
    (ROUTE_UMOINER_OUT, ROUTE_UMOINER_IN,  70,   60,   80,   65),
    (ROUTE_RUIRU_OUT,   ROUTE_RUIRU_IN,   130,  110,  150,  120),
    (ROUTE_JUJA_OUT,    ROUTE_JUJA_IN,    160,  140,  180,  150),
    (ROUTE_THIKA_OUT,   ROUTE_THIKA_IN,   200,  170,  230,  190),
]

FARES = []
_fare_counter = 1
for (_rout, _rin, _peak, _offpeak, _late, _wkend) in _FARE_DEFS:
    for _rid in (_rout, _rin):
        for _row in [
            {"fare_type": "peak",       "day_type": 0, "amount_kes": _peak,
                "valid_from": "06:00", "valid_until": "09:00"},
            {"fare_type": "peak",       "day_type": 0, "amount_kes": _peak,
                "valid_from": "16:30", "valid_until": "19:30"},
            {"fare_type": "off_peak",   "day_type": 0, "amount_kes": _offpeak,
                "valid_from": "09:00", "valid_until": "16:30"},
            {"fare_type": "late_night", "day_type": 0, "amount_kes": _late,
                "valid_from": "21:00", "valid_until": "23:59"},
            {"fare_type": "weekend",    "day_type": 5, "amount_kes": _wkend,
                "valid_from": "00:00", "valid_until": "23:59"},
            {"fare_type": "weekend",    "day_type": 6, "amount_kes": _wkend,
                "valid_from": "00:00", "valid_until": "23:59"},
        ]:
            FARES.append({"id": f"a3000000-0000-0000-0000-{_fare_counter:012d}",
                          "route_id": _rid, **_row})
            _fare_counter += 1


PAYMENT_METHODS = []
ALL_ROUTE_IDS = [r["id"] for r in ROUTES]
_pm_counter = 1
for _rid in ALL_ROUTE_IDS:
    for _method in ("cash", "mpesa"):
        PAYMENT_METHODS.append({"id": f"a4000000-0000-0000-0000-{_pm_counter:012d}",
                                "route_id": _rid, "method": _method})
        _pm_counter += 1

PUBLIC_HOLIDAYS = [
    {"id": "a5000000-0000-0000-0000-000000000001", "name": "New Year's Day",
        "holiday_date": "2026-01-01", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000002", "name": "Good Friday",
        "holiday_date": "2026-04-03", "is_recurring": False, "year": 2026},
    {"id": "a5000000-0000-0000-0000-000000000003", "name": "Easter Monday",
        "holiday_date": "2026-04-06", "is_recurring": False, "year": 2026},
    {"id": "a5000000-0000-0000-0000-000000000004", "name": "Labour Day",
        "holiday_date": "2026-05-01", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000005", "name": "Madaraka Day",
        "holiday_date": "2026-06-01", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000006", "name": "Mashujaa Day",
        "holiday_date": "2026-10-20", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000007", "name": "Jamhuri Day",
        "holiday_date": "2026-12-12", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000008", "name": "Christmas Day",
        "holiday_date": "2026-12-25", "is_recurring": True,  "year": None},
    {"id": "a5000000-0000-0000-0000-000000000009", "name": "Boxing Day",
        "holiday_date": "2026-12-26", "is_recurring": True,  "year": None},
]


_OCC_PROFILE = {
    5:  (0.35, 0.20, 0.15), 6:  (0.70, 0.40, 0.25), 7:  (0.95, 0.55, 0.30),
    8:  (0.98, 0.60, 0.35), 9:  (0.75, 0.65, 0.40), 10: (0.55, 0.70, 0.50),
    11: (0.45, 0.72, 0.55), 12: (0.50, 0.75, 0.60), 13: (0.55, 0.70, 0.58),
    14: (0.50, 0.65, 0.55), 15: (0.55, 0.60, 0.50), 16: (0.80, 0.65, 0.45),
    17: (0.98, 0.70, 0.50), 18: (0.97, 0.68, 0.48), 19: (0.80, 0.60, 0.42),
    20: (0.55, 0.50, 0.35), 21: (0.35, 0.38, 0.28), 22: (0.20, 0.25, 0.18),
}

OCCUPANCY = []
_occ_counter = 1
for _rid in ALL_ROUTE_IDS:
    for _hour, (_wd, _sat, _sun) in _OCC_PROFILE.items():
        for _dow in range(5):
            OCCUPANCY.append({"id": f"a6000000-0000-0000-0000-{_occ_counter:012d}",
                              "route_id": _rid, "day_of_week": _dow, "hour_slot": _hour,
                              "avg_load_factor": _wd, "sample_count": 120})
            _occ_counter += 1
        OCCUPANCY.append({"id": f"a6000000-0000-0000-0000-{_occ_counter:012d}",
                          "route_id": _rid, "day_of_week": 5, "hour_slot": _hour,
                          "avg_load_factor": _sat, "sample_count": 60})
        _occ_counter += 1
        OCCUPANCY.append({"id": f"a6000000-0000-0000-0000-{_occ_counter:012d}",
                          "route_id": _rid, "day_of_week": 6, "hour_slot": _hour,
                          "avg_load_factor": _sun, "sample_count": 40})
        _occ_counter += 1

APP_SETTINGS = [
    {"key": "corridor_surge_enabled",      "value": "true",
        "description": "Toggle corridor surge pricing globally"},
    {"key": "late_night_threshold_hour",   "value": "21",
        "description": "Hour (24h) after which late_night fare applies"},
    {"key": "transfer_search_max_legs",    "value": "2",
        "description": "Maximum transfer legs in route search"},
    {"key": "default_currency",            "value": "KES",
        "description": "ISO 4217 currency code"},
    {"key": "fare_correction_review_days", "value": "7",
        "description": "Days before unreviewed fare corrections auto-expire"},
    {"key": "stage_alias_fuzzy_threshold", "value": "0.75",
        "description": "Minimum similarity score (0-1) for fuzzy stage alias matching"},
]
