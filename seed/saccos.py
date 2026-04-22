from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sacco import Sacco, SaccoAlias, VehicleType, OperatingStatus, AliasType
from datetime import datetime, timezone


async def seed_saccos(db: AsyncSession) -> dict:
    saccos_data = [
        Sacco(
            name="Super Metro",
            vehicle_type=VehicleType.SEATER_32,
            is_electric=False,
            terminus_area="OTC Terminal",
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=4.5,
            comfort_rating=4.2,
            is_verified=True,
            last_confirmed_at=datetime.now(timezone.utc)
        ),
        Sacco(
            name="Kenya Mpya",
            vehicle_type=VehicleType.SEATER_32,
            is_electric=False,
            terminus_area="GPO Drop-off",
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=3.2,
            comfort_rating=3.0,
            is_verified=True,
            last_confirmed_at=datetime.now(timezone.utc)
        ),
        Sacco(
            name="Metro Trans",
            vehicle_type=VehicleType.ELECTRIC,
            is_electric=True,
            terminus_area="GPO Pick-up",
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=4.2,
            comfort_rating=4.5,
            is_verified=True,
            last_confirmed_at=datetime.now(timezone.utc)
        ),
        Sacco(
            name="Joy Kenya",
            vehicle_type=VehicleType.SEATER_32,
            is_electric=False,
            terminus_area="River Road",
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=3.2,
            comfort_rating=3.2,
            is_verified=True,
            last_confirmed_at=datetime.now(timezone.utc)
        ),
        Sacco(
            name="Paradiso",
            vehicle_type=VehicleType.SEATER_14,
            is_electric=False,
            terminus_area="OTC Stage",
            operating_status=OperatingStatus.ACTIVE,
            safety_rating=4.0,
            comfort_rating=4.8,
            is_verified=True,
            last_confirmed_at=datetime.now(timezone.utc)
        ),
    ]

    seeded = []
    for s in saccos_data:
        seeded.append(await db.merge(s))

    await db.flush()

    aliases = [
        SaccoAlias(sacco_id=seeded[0].id, alias="SM", alias_type=AliasType.ABBREVIATION),
        SaccoAlias(sacco_id=seeded[1].id, alias="Mpya", alias_type=AliasType.COLLOQUIAL),
        SaccoAlias(sacco_id=seeded[2].id, alias="Metro", alias_type=AliasType.COLLOQUIAL),
        SaccoAlias(sacco_id=seeded[4].id, alias="Para", alias_type=AliasType.COLLOQUIAL),
    ]

    for a in aliases:
        await db.merge(a)

    await db.commit()

    return {s.name: s for s in seeded}