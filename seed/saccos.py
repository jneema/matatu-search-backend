from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sacco import Sacco, SaccoAlias, VehicleType, OperatingStatus, AliasType
from datetime import datetime, timezone


async def seed_saccos(db: AsyncSession) -> dict:
    def make(name, vtype, electric, terminus, safety, comfort, verified=True):
        return Sacco(
            name=name,
            vehicle_type=vtype,
            is_electric=electric,
            terminus_area=terminus,
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=safety,
            comfort_rating=comfort,
            is_verified=verified,
            last_confirmed_at=datetime.now(timezone.utc),
        )

    S32 = VehicleType.SEATER_32
    S14 = VehicleType.SEATER_14
    EL = VehicleType.ELECTRIC

    saccos_data = [
        make("Super Metro",   S32, False, "OTC Terminal",       4.5, 4.2),
        make("Kenya Mpya",    S32, False, "GPO Drop-off",       3.2, 3.0),
        make("Metro Trans",   EL,  True,  "GPO Pick-up",        4.2, 4.5),
        make("Joy Kenya",     S32, False, "River Road",         3.2, 3.2),
        make("Paradiso",      S14, False, "OTC Stage",          4.0, 4.8),
        make("Zuri",          S32, False, "OTC Terminal",       4.3, 4.0),
        make("Citi Hoppa",    S32, False, "OTC Terminal",       3.8, 3.6),
        make("2NK",           S32, False, "OTC Terminal",       3.5, 3.4),
        make("Nazigi",        S32, False, "River Road",         3.3, 3.2),

        make("Nicco",         S32, False, "River Road",         3.0, 2.9),
        make("MTN",           S32, False, "OTC Terminal",       3.1, 3.0),
        make("Forward Travellers", S32, False, "OTC Terminal",  3.4, 3.2),
        make("Umoinner",      S32, False, "OTC Terminal",       3.0, 2.8),
        make("Neno",          S32, False, "OTC Terminal",       2.9, 2.8),
        make("Classic",       S32, False, "OTC Terminal",       3.2, 3.0),
        make("Zimmerman Express", S32, False, "OTC Terminal",   3.3, 3.1),
        make("KU Shuttle",    S14, False, "Kenyatta University", 3.6, 3.5),
        make("Kasarani Link", S32, False, "OTC Terminal",       3.1, 3.0),
        make("Juja Express",  S32, False, "OTC Terminal",       3.5, 3.3),
        make("Ruiru Star",    S32, False, "OTC Terminal",       3.2, 3.0),
        make("Sasa Sawa",     S32, False, "Roysambu (TRM)",     3.0, 2.9),
        make("Matatu 45",     S32, False, "River Road",         2.8, 2.7),
        make("Matatu Bypass", S32, False, "OTC Terminal",       2.9, 2.8),
        make("Clay City Link", S32, False, "OTC Terminal",       3.0, 2.9),
        make("Thika Express", S32, False, "OTC Terminal",       3.6, 3.4),
    ]

    seeded = []
    for s in saccos_data:
        merged = await db.merge(s)
        seeded.append(merged)

    await db.flush()

    by_name = {s.name: s for s in seeded}

    aliases = [
        ("Super Metro",       "SM",           AliasType.ABBREVIATION),
        ("Kenya Mpya",        "Mpya",         AliasType.COLLOQUIAL),
        ("Metro Trans",       "Metro",        AliasType.COLLOQUIAL),
        ("Paradiso",          "Para",         AliasType.COLLOQUIAL),
        ("Zuri",              "Zuri Bus",     AliasType.COLLOQUIAL),
        ("Citi Hoppa",        "City Hoppa",   AliasType.COLLOQUIAL),
        ("2NK",               "2NK Sacco",    AliasType.COLLOQUIAL),
        ("Nicco",             "Route 45",     AliasType.COLLOQUIAL),
        ("MTN",               "MTN Matatu",   AliasType.COLLOQUIAL),
        ("Forward Travellers", "Forward",      AliasType.COLLOQUIAL),
        ("Umoinner",          "Umo",          AliasType.COLLOQUIAL),
        ("Juja Express",      "Juja Direct",  AliasType.COLLOQUIAL),
        ("Thika Express",     "Thika Direct", AliasType.COLLOQUIAL),
        ("Zimmerman Express", "Zim Express",  AliasType.COLLOQUIAL),
        ("KU Shuttle",        "KU Bus",       AliasType.COLLOQUIAL),
        ("Sasa Sawa",         "Sawa Mall",    AliasType.COLLOQUIAL),
    ]

    for sacco_name, alias_str, atype in aliases:
        sacco = by_name.get(sacco_name)
        if sacco:
            await db.merge(SaccoAlias(
                sacco_id=sacco.id,
                alias=alias_str,
                alias_type=atype,
            ))

    await db.commit()
    return by_name
