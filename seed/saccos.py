from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sacco import Sacco, SaccoAlias, VehicleType, OperatingStatus, AliasType
from datetime import datetime, timezone


async def seed_saccos(db: AsyncSession) -> dict:
    saccos_data = [
        Sacco(name="Super Metro", vehicle_type=VehicleType.SEATER_32, is_electric=False, terminus_area="OTC", operating_status=OperatingStatus.ACTIVE, safety_rating=3.8, comfort_rating=4.2, is_verified=True, last_confirmed_at=datetime.now(timezone.utc)),
        Sacco(name="Kenya Mpya", vehicle_type=VehicleType.SEATER_32, is_electric=False, terminus_area="GPO", operating_status=OperatingStatus.ACTIVE, safety_rating=3.5, comfort_rating=3.5, is_verified=True, last_confirmed_at=datetime.now(timezone.utc)),
        Sacco(name="Metro Trans", vehicle_type=VehicleType.ELECTRIC, is_electric=True, terminus_area="GPO", operating_status=OperatingStatus.ACTIVE, safety_rating=4.2, comfort_rating=4.5, is_verified=True, last_confirmed_at=datetime.now(timezone.utc)),
        Sacco(name="Joy Kenya", vehicle_type=VehicleType.SEATER_32, is_electric=False, terminus_area="River Road", operating_status=OperatingStatus.ACTIVE, safety_rating=3.2, comfort_rating=3.2, is_verified=True, last_confirmed_at=datetime.now(timezone.utc)),
        Sacco(name="Paradiso", vehicle_type=VehicleType.SEATER_14, is_electric=False, terminus_area="OTC", operating_status=OperatingStatus.ACTIVE, safety_rating=4.0, comfort_rating=4.8, is_verified=True, last_confirmed_at=datetime.now(timezone.utc)),
    ]
    for s in saccos_data:
        db.add(s)
    await db.commit()

    aliases = [
        SaccoAlias(sacco_id=saccos_data[0].id, alias="super met", alias_type=AliasType.COLLOQUIAL),
        SaccoAlias(sacco_id=saccos_data[0].id, alias="metro", alias_type=AliasType.COLLOQUIAL),
        SaccoAlias(sacco_id=saccos_data[2].id, alias="metro trans", alias_type=AliasType.COLLOQUIAL),
        SaccoAlias(sacco_id=saccos_data[3].id, alias="joy", alias_type=AliasType.COLLOQUIAL),
    ]
    for a in aliases:
        db.add(a)
    await db.commit()

    result = {s.name: s for s in saccos_data}
    print(f"  seeded {len(saccos_data)} saccos and {len(aliases)} aliases")
    return result